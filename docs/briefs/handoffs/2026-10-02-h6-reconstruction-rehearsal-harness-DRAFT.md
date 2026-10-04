# H6: settlement reconstruction-rehearsal harness (synthetic, disposable stores)

**Type:** cc_handoff (worker harness card)

**Status:** DRAFT, 2026-10-02. Drafted by a coordinator worker for the deployment coordinator to freeze; not dispatched. The coordinator answers §12's open decisions, commits the frozen revision under the committed-handoff rule and records its SHA before any worker starts.

**Executor:** one worker named at freeze (the coordinator's plan lists it as remote lane P: branch-only, no PR). It is the single writer of `claude/h6-rehearsal-harness` (proposed), cut from `origin/main` at the frozen revision.

**Coordinator:** the deployment coordinator ("Coordinating parallel Claude sessions (2)"). It proposes the CAP S1/S2 rows for acceptance, reviews the diff and owns PRs and the ledger.

**Owner this card narrows:** [staged acceptance H6](2026-09-27-staged-acceptance-handoffs.md#h6--settlement-collection-and-reconstruction-rehearsal) (`:411-446`). Its state row reads "Collection READY ON CP-2; rehearsal harness READY" (`:52`), and "the rehearsal harness may be prepared before CP-2" (`:422`). This card is the harness half only; collection is operator-performed.

```yaml authority
seat: worker
parent: docs/briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push]
constraints:
  - no_main_write
  - no_merge
  - no_pr_open
  - no_linux_or_ci_dispatch
  - new_test_files_only
  - no_existing_module_or_test_edit
  - synthetic_fixtures_only
  - no_private_originals_read_or_committed
  - disposable_stores_only
  - no_account_api_or_route_access
  - no_operator_signing_entry_point
  - single_writer
  - stop_at_coordinator_return
acceptance:
  - tests/ops/test_settlement_reconstruction_rehearsal.py
  - tests/ops/test_book_settlement.py
  - tests/ops/test_book_owner_settlement_integration.py
  - tests/ops/test_account_close_assembler.py
  - tests/ops/test_account_close_calculation.py
  - tests/ops/test_account_close_evidence.py
```

`test_settlement_reconstruction_rehearsal.py` and its support module `tests/ops/settlement_rehearsal.py` are new (§2). The other five are existing settlement tests that must pass unchanged.

## 0. Phase 0: premise and Rule-0 reads

1. **Premise.** HEAD is the frozen revision on `origin/main` (as of 2026-10-02, `6de7bf9`). No `.env`. `git status` clean. No private root is mounted or read.
2. **Rule-0 reads** (read them; do not infer them):
   - The T07 procedure `docs/briefs/handoffs/2026-09-21-tradeify-t07-manual-settlement-procedure.md`: "No silent reset" (`:20`), the S2 report facts (`:21`), the consumer rehearsal cases (a)–(e) (`:23`), synthetic fixtures never derived from real bytes (`:27`), and the missing operator entry point (`:52`).
   - The attended settlement contract `docs/spec/2026-09-15-tradeify-attended-settlement-contract.md`: evidence rules (`:53-59`; a missing CSV row is not proof of no activity, `:59`), corrections and restore (`:194-212`), required acceptance traces (`:214-230`).
   - The CAP record `docs/briefs/phase4-preparation/2026-09-16/capability-decision.md`: addendum S1–S5 (`:538-542`), the three S2 facts (`:579-599`), and the anchor note (`:325`).
   - Consumer code, read only:
     - `ops/c1_rail/account_close_evidence.py` (`parse_cash_report` `:134`, `parse_cash_windows` `:182`, `parse_balance_history` `:224`, `verify_source_manifest` `:255`, `verify_history_coverage` `:304`);
     - `ops/c1_rail/account_close_ledger.py` (`reconcile` `:23`);
     - `ops/c1_rail/account_close_assembler.py` (`assemble` `:36`);
     - `ops/c1_rail/account_close_calculation.py` (`EVIDENCE_FRESHNESS` `:23`, `verify_package` `:421`, `calculate_close` `:440`);
     - `ops/c1_rail/book_settlement.py` (`CHALLENGE_LIFETIME` `:41`; `SettlementStore` `:174`: `boot` `:375`, `reconcile_restore` `:468`, `bootstrap_b7` `:500`, `issue_challenge` `:620`, `submit` `:679`, `record_revision` `:837`, `resolve_invalidation` `:881`, `settled_close` `:932`);
     - `ops/c1_rail/book_account_owner.py` (`boot` `:375`, `open_settlement` `:613`).
   - Synthetic generators to reuse, not copy: `tests/ops/account_close_test_support.py` (`package` `:41`, `_bind_csv_reports` `:106`, `b7_cash_history` `:159`, `b7_previous_package` `:174`); `tests/ops/test_book_settlement.py` (`Operator` `:56`, `b7_seal` `:70`, `seat` `:94`, `boot` `:105`).
   - The disposable-store precedent: `tests/ops/test_attended_incident_rehearsal.py:1-30` (H5b).
3. **Store facts that bind the harness:** `SettlementStore.boot` refuses an existing empty file (`book_settlement.py:423-427`), so each scenario's store path must not exist beforehand. The account owner exposes no wrapper for `bootstrap_b7`, `reconcile_restore` or `resolve_invalidation`; existing tests call the store directly (`test_book_owner_settlement_integration.py:95`, `:233`).

## 0.5. Routing and clarifying questions

Claude worker lane: settlement authority path; tests only. Not GLM: the harness composes the settlement trust chain (signing, revision quarantine), and its later private run touches account bytes. No secrets, `.env`, account data or Pine. The coordinator answers §12 H-1–H-8 at freeze; anything Phase 0 needs and §12 leaves open returns as NEEDS_CONTEXT.

## 1. Goal

One traced, timed rehearsal procedure that drives the existing settlement consumers end to end on disposable stores, over synthetic report bytes: an isolated anchor ingestion and a subsequent close, correction refusal and restoration, and the missing-data cases. Its output is a consumer trace with record IDs and per-step durations. The same procedure is ready to run later on the operator's machine against private originals after CP-2 confirms the target and the operator has collected them (H6 `:424-430`). That run is not part of this dispatch.

## 2. Scope (new test files only)

- **`tests/ops/settlement_rehearsal.py`** (location: H-1): the procedure. Each scenario boots a **fresh** store under a temporary root, runs the consumer path, and returns a trace of steps, digests, record and receipt IDs, refusal names and monotonic durations. Signing uses a disposable rehearsal key trusted only in that store (H-3). The three S2 source facts (report timezone, the `Date` meaning after rollover, query-bound semantics) are explicit parameters recorded in every trace, never defaults hidden in code (H-4).
- **`tests/ops/test_settlement_reconstruction_rehearsal.py`:** the §4 scenarios over synthetic fixtures built with the existing generators. A private-input case may be present but **skips** unless an operator-set root variable names a private directory (H-2; the repository's vendor-skip posture). Under this dispatch it is never run with that variable set.

## 3. Method

- Compose the existing consumers; never re-implement a check or weaken one. A behavior the consumers lack is a finding, not a harness feature.
- Tests first: each scenario is written and shown failing (no harness) with a launcher record, then passing.
- Synthetic fixtures only, never derived from real bytes (T07 `:27`); dates in ratified calendar months, as the existing tests arrange (H-8).

## 4. Acceptance checks (falsifier-first)

**H:** the existing consumers, driven in sequence on disposable stores, reconstruct an anchor and a subsequent close from report bytes and refuse every correction and missing-data case by name without state advance, within a measured procedure time. **Reject if** a scenario cannot be made to fail first, an existing settlement test changes outcome, or any existing file changes. **Revert trigger:** any byte outside the two new files and the return note.

Scenarios (H6 `:424-430`; T07 (a)–(e) `:23`; contract traces `:214-230`):
1. **Anchor:** a synthetic sealed B7 is authenticated and re-derived, then seated as the first head by `bootstrap_b7` in a fresh store; a relabelled inventory refuses. The trace holds the seal digest and the head ID.
2. **Subsequent close:** synthetic exports are assembled, verified, challenged, signed with the rehearsal key and submitted, giving exactly one settled close chained on the anchor. The trace holds the package digest, challenge, receipt and settled-close mode.
3. **Correction refusal:** a later export that contradicts the accepted close (a revised transaction ID; a late-added historical transaction) is refused, not merged. Both versions are retained, dependants invalidated, halt (contract `:227`).
4. **Restoration:** a crash between acceptance and receipt restarts restore-pending and reconciles to the same single acceptance (contract `:229`). `resolve_invalidation` with a review reseats the chain; revising the B7 head needs a new seal. No silent predecessor reset (T07 `:20`).
5. **Missing data:** an empty history or missing day refuses without copying the previous balance (contract `:223`); a missing source role or coverage gap refuses by name without state advance.
6. **Duplicate and out-of-order rows:** refused or deduplicated by transaction ID exactly as the consumers already do (T07 (e)).
7. **Timing:** per-step and whole-procedure durations are recorded and reported against `CHALLENGE_LIFETIME` 300 s and `EVIDENCE_FRESHNESS` 30 min. They are labelled machine time on synthetic bytes, not the operator's export time.
8. **Disposability:** every store path is fresh and outside the repository; a pre-existing path refuses; no file under the repository changes during a run.

Runs, each with its launcher record: the acceptance set; `tests/ops`; `python -I scripts/fp.py check`; `git diff --check`; `git diff --name-status origin/main...HEAD` (new files only).

## 5. Forbidden

- Reading, copying, hashing or quoting any private original or private root (`local_artifacts/t07-reads-2026-09/`, the lab `private_overrides/op1/` roots), or running the private-input case.
- Editing any existing module or test, including the settlement consumers and their generators.
- Building an operator-facing sign/submit entry point, or using any operator key (the missing tool is a decision H6 unlocks: T09 or tooling, H6 `:443-444`).
- Account, broker, API or route access; any collection step.
- Resolving the three S2 facts by assumption: they stay parameters, labelled.
- Linux runs, CI changes, PRs, merges, pushes to `main`.
- `core/`, `lab/`, Pine.

## 6. Return (status taxonomy)

Return DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT or BLOCKED. The coordinator's verdict is RESOLVED or FALSIFIED (named items). The return holds:
- branch and head SHA; the name list (new files only);
- per scenario, the fail-first and pass record IDs and one example trace (synthetic values only);
- the timing table (labelled machine time);
- the S2-fact parameter set each scenario ran under;
- the consumer gaps found, each as a finding for the coordinator, not a fix;
- concerns.

## 7. Stop conditions (return to the coordinator; do not work around)

- A scenario needs an existing module or test changed, or a consumer check weakened.
- A consumer behavior contradicts the settlement contract or T07.
- Any step would read private bytes or touch an account.
- Two failed corrections of the same issue (AGENTS.md).
- **Operator review-round rule (2026-10-02):** after more than three review rounds that each return two or more P1/P2 findings, stop folding; the coordinator adjudicates a rewrite or a narrower scope.
- **Single writer:** only the executor writes `claude/h6-rehearsal-harness`. A second writer appearing is a stop.

## 8. Out of scope and decision unlocked

**Out of scope:** operator collection (READY ON CP-2); the private run on originals; resolving the S2 facts; the S3/B7 predecessor choice; an operator-facing entry point; T07 acceptance.

**Unlocked:** an accepted harness lets the private rehearsal run on the operator's machine as soon as collection lands, so H6's decisions (H6 `:442-444`: the S3/B7 predecessor choice, and whether a sign/submit entry point is scoped to T09 or tooling) wait only on the private trace. CAP S1/S2 rows are proposed by the coordinator from that trace (H6 `:440`), not from this synthetic return.

## 9. Dispatch record

- Base: the frozen `origin/main` revision named at freeze.
- Dispatch revision: the commit that freezes this card; the coordinator records it.

## 10. Audit hooks (runnable)

```bash
# Card form and authority. Expected: RESULT: well-formed; exit 0.
python -I scripts/fp.py python scripts/check_brief.py --type handoff docs/briefs/handoffs/2026-10-02-h6-reconstruction-rehearsal-harness-DRAFT.md
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-02-h6-reconstruction-rehearsal-harness-DRAFT.md
# Premise (Git Bash), in the executor worktree.
test ! -e .env && echo "no .env" || echo "FAIL: .env present"
grep -n "CHALLENGE_LIFETIME =\|^class SettlementStore\|def bootstrap_b7\|def reconcile_restore" ops/c1_rail/book_settlement.py
grep -n "EVIDENCE_FRESHNESS =" ops/c1_rail/account_close_calculation.py
# Scope at return: only new files under tests/ops.
git diff --name-status origin/main...HEAD
```

## 11. Pre-mortem (README rule)

- **Loop cost:** one Windows test loop; no Linux.
- **Decisions the executor will hit:** H-1 (location), H-3 (signing key), H-4 (S2 parameters). Ruled at freeze.
- **What makes it moot:** CP-2 failing to confirm a qualifying completed target, or an S2 fact that is unsupported and decisive (H6 stop condition `:436`).
- **Measurements the return fills in:** per-scenario records, example traces and the machine-time table.

## 12. Open decisions (for the coordinator at freeze)

- **H-1 Location.** `tests/ops/` support module plus test (this draft), or a runnable script. `tools/` is governance-layer and may not import `ops/` without reclassification (`REPO_MAP.md:65`, `:71-73`); `scripts/` needs a layer entry and the scripts table.
- **H-2 Private-input mode.** Include the skipped private case now, or defer it to a separate operator-machine card after CP-2.
- **H-3 Signing.** A disposable rehearsal key trusted only in the disposable store (this draft), or the operator's key, which needs the entry point H6 leaves to T09 or tooling.
- **H-4 S2 defaults.** The synthetic parameter set (the code's current assumptions: caller-supplied report timezone, `Date` unused, inclusive local query bounds), and how a later private run labels them until a primary source resolves S2 (T07 `:21`).
- **H-5 Anchor meaning.** No document defines "anchor". This draft reads it as the head `bootstrap_b7` seats from a sealed B7 (CAP `:325`: September 14 cannot be promoted to a mandatory anchor). The coordinator confirms.
- **H-6 Timed procedure.** Which steps the synthetic timing covers and where the private run's operator steps are timed.
- **H-7 Executor.** Remote lane P (branch-only) or another worker; the card is lane-neutral.
- **H-8 Calendar.** Synthetic dates restricted to ratified months, or the tests' `ratified_at` override pattern.
