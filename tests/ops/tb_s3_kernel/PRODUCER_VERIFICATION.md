# Producer verification — 2026-09-13

Scope: PR #368, offline E1–E3 producer only. Starting extraction b0103dc;
user's main-merge head 0dcc183 was preserved. Production code is unchanged.

Producer SHA-256: dbc3e640052d7d621507948941ec01f690fffdfd55f4081cc780687cf00ba32b

## Local and independent evidence

- Producer suite: 37 passed. New regressions were observed failing before their
  corresponding fixes; additional sequence characterizations cover global fences,
  delayed delivery, detached maps and unsupported transitions.
- Full current-branch ops suite: 614 passed, 13 skipped; two existing seaborn warnings.
  The final synchronous-request logging preservation was subsequently exercised
  by the producer suite and downstream compatibility run.
- Repository check-tier gates passed with normal absent-private-data notices.
- Focused pylint errors-only passed with the worktree on PYTHONPATH. The broader
  advisory lint run reports style/complexity warnings; it is not represented as clean.
- Independent reviewer accepted the complete producer candidate with no blocking
  findings, independently repeated the 37 tests, and checked 50 seeded sequences
  of 100 events for position, gross quantity, tranche conservation and consumed owners.

Reproduce current-branch tests:

```text
python -m pytest tests/ops/test_tb_s3_evidence_contract.py -q
python -m pytest tests/ops -q
python scripts/gate_manifest.py --tier check
```

## Downstream migration remains blocked

An in-memory substitution of this producer into #370 head b563723's broker module
ran its unchanged extracted suite: **384 passed, 9 failed**. No #369/#370 files were
modified. This is an intentionally exposed migration gap, not integrated acceptance.

Six failing adversarial cases previously relied on malformed normal route calls:

- test_restart_halts_on_an_orphan_working_order_and_never_cancels_it
- test_orphan_cancel_fill_race_retains_ownership_through_recovery (two variants)
- test_partial_orphan_recovery_counts_broker_exposure_and_retries_same_operation
- test_full_close_can_retry_residual_first_observed_after_dispatch
- test_change_fill_restore_cannot_fabricate_an_owned_fill (kind-flat variant)

These need explicit adversarial broker/evidence injection that preserves the intent
of the original tests, not removal of their safety assertions.

Three failing cases expose the consumer's stable-one-lot-per-entry assumption:

- test_full_fill_exit_owns_the_entry_remainder_and_its_late_fill (two variants)
- test_consumed_amendment_does_not_strand_a_later_partial_entry_fill

#369 must consume generation-specific fill IDs, retained protection owners and
execution-tranche allocations, then independently re-review late-fill ownership,
quarantine, scope expansion, restart/reordering and unsupported divergent closes.
A passing producer is not permission to waive any of those failures or merge #370.

Live producer equivalence, L-2 qualification and all operator gates remain owed.

## Subsequent #369 migration

The nine exposed migration failures are repaired in #369 using explicit adversarial
injection and generation-aware consumer allocation. #369 also adds optional close
request attribution to Reduction. See `PRIMITIVE_VERIFICATION.md` for the updated
combined verification; the #368 counts and revision above remain historical.
