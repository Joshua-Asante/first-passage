# Evidence and Calculation Component Implementation Plan

> **For agentic workers:** Execute with superpowers:executing-plans; use superpowers:subagent-driven-development when bounded delegation is useful and authorized. Preserve the behavioral contract and integration owner. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Repair evidence ingestion and close calculation, then publish them as independently reviewable components of the approved PR 395 split.

**Architecture:** `account_close_evidence.py` owns report parsing, source manifests and coverage checks. `account_close_calculation.py` owns package invariants and returns a proposed close or refusal without persistence. The assembler composes evidence and arithmetic; the existing durable owner calls the pure calculation under its transaction.

**Tech Stack:** Python 3.11-compatible dataclasses, Decimal, zoneinfo, CSV/JSON, pytest; existing shared protection law.

**Spec:** Approved PR 395 component split in PR 396; `docs/spec/2026-09-15-tradeify-attended-settlement-contract.md` remains governing. P6 in PR 397 remains proposed.

## Global Constraints

- Preserve policy constants, pinned calendar artifacts and the operator-signed acceptance contract.
- Original evidence bytes remain authoritative; source-account fields for opaque captures are operator transcriptions from those specific views, not machine verification.
- Old package shapes lacking per-source account identity or per-window file bindings refuse; do not silently infer missing evidence.
- The integration coordinator owns combined acceptance. No component result grants activation.

## Task 1: Complete bound evidence

Files: `ops/c1_rail/account_close_evidence.py`, `account_close_assembler.py`,
`book_settlement.py`, and evidence/assembler/settlement tests.

Interface: `SourceFile` carries role, file name, original bytes, aware capture time,
query labels/completion and observed `account_id`. `parse_cash_windows` produces
deduplicated normalized rows and a collection report. `verify_source_manifest`
checks source byte hashes, account bindings, unique roles/files, required independent
artifacts. `verify_history_coverage` binds each complete window to its cash source,
measures limits in the displayed timezone and checks continuous inception-to-capture coverage.

- [ ] Reproduce omitted cash-window source, reused close-equity bytes in either role order, autumn-DST limit, future rows, naive timestamps and wrong/missing per-source accounts.
- [ ] Add tests before changing implementations:

```python
with pytest.raises(AssemblyError, match="after capture"):
    parse_cash_windows([future_row_file], report_tz=CT)
assert verify_package(with_missing_window_source, remaining_bytes, **context) is not None
assert verify_package(valid_fourteen_local_days_across_fall_back, source_bytes, **context) is None
```

- [ ] Implement source checks once and route assembler/verifier through them. Window metadata adds `file`; source metadata adds `account_id`. Require aware timestamps before UTC conversion. Parse each row's capture chronology before deduplication.
- [ ] Exercise producer-to-verifier mutations, including empty source windows and duplicate exports; keep evidence collection independent of database/signing modules.

## Task 2: Pure close calculation

Files: `ops/c1_rail/account_close_calculation.py`, assembler and owner adapters,
`tests/ops/test_account_close_calculation.py`, existing integration tests.

Interface: `calculate_close(package, sources, ..., policy)` returns immutable
`ProposedClose(equity, peak, mode_next)` or `Refusal`. Existing `verify_package`
retains its reason-or-None interface for callers. All validation precedes proposal
creation. Durable owner alone persists the proposal and sources.

- [ ] Reproduce ordinary-predecessor record-only catch-up with fresh later-session rows and finite Decimal values overflowing float conversion.
- [ ] Test retained transaction deletion/change, newly discovered old-session activity, sequential catch-up after the inventory already contains later transactions, and current-scope future-session refusal.
- [ ] Keep previously observed inventory immutable; allow newly observed later-session rows in record-only, but do not silently accept added rows for previously settled sessions. Validate finite equity/peak conversions before calling shared policy.
- [ ] Extract the invariant pipeline and proposal calculation from the durable store; remove assembler's dependency on the store. Verify pure component import paths and actual store integration.

## Task 3: Review and publication

- [ ] Run focused evidence/calculation/assembler/owner tests with `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 py -3.13 -m pytest`, then the ops suite.
- [ ] Independent review of complete behavior and unchanged consumers; address findings and reverify affected contracts.
- [ ] Publish the linear review stack: calendar PR 396, evidence PR 398, then calculation on evidence. Evidence itself has no calendar imports; stacking preserves the approved review order without bundling component diffs. Preserve PR 395 as integration reference.

## Verified implementation checkpoint

All eight scoped findings are repaired: window/source binding, conditional source
independence, local-date/DST limit, row/capture ordering, source-account binding,
aware event timestamps, ordinary-predecessor catch-up, and numeric ranges.
Package inputs are explicitly versioned as v2 for the stronger required bindings.

Fifteen initial regression cases reproduced the defects before implementation.
Independent review found three further boundary gaps (dashboard/parser numeric
ranges, unknown scope, out-of-query rows); each was reproduced, repaired, and
accepted on re-review. The reviewer independently ran 93 relevant tests.

Final integration workspace at base bd41cb6 plus these changes and calendar 7e83e1b:
226 affected tests passed; full ops 1,968 passed, 15 skipped, two upstream seaborn
warnings. Python 3.13 with `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`. The evidence-only
extraction passed all 40 standalone evidence tests.

The known source qualification limits and three owner defects below remain open.
Store adapters and store integration regressions remain on the integration branch
for the later owner slice, not in either independent component PR.

## Deferred durable-owner findings

Revision source retention, the pre-challenge signing timestamp cycle, and B7's
weekday-specific reopen boundary remain durable-owner work. This repair does not
claim those gates or actual report qualification are complete.
