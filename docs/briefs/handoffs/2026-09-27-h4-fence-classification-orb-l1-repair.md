# H4 — Fence classification (synthetic repair) and the ORB L1 qualification-replay correction — worker card

**Status:** PREPARED 2026-09-27 by [handoff H3](2026-09-27-staged-acceptance-handoffs.md#h3--orb-lifecycle-and-fence-disposition-owner-text-for-ruling-7-h4-card). **Not dispatched.** It becomes dispatchable only after the coordinator accepts:
- H3's owner text (the dated 2026-09-27 amendments to the rail spec, the replay spec and the edition pre-registration);
- H3's [disposition note](../../notes/2026-09-27-orb-fence-ruling6-disposition.md);
- this card, including its answer to disposition Q3.

At dispatch the coordinator records the dispatch revision in §10 and runs the pre-dispatch read ([surface-allocation ADR](../../adr/2026-07-14-cc-cursor-surface-allocation.md#decision), *Action classes and the authority block*).

**Parent:** [staged acceptance handoff set, card H4](2026-09-27-staged-acceptance-handoffs.md#h4--fence-classification-synthetic-repair-plus-the-orb-l1-replay-correction). The parent file carries no authority block, so it bounds nothing beyond this card's own seat checks.

**Authority:** [campaign §59 Ruling 7](../programs/2026-09-03-seven-strategy-select-campaign-state.md#ruling-7--orb-lifecycle-l1-reaffirmed-and-the-account-fence-classification-contract-2026-09-27), in the relayed words: "Authorize the bounded synthetic repair and corresponding specification/replay corrections, retaining real-producer and route acceptance obligations." This card grants nothing its dispatcher lacks.

```yaml authority
seat: worker
parent: docs/briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push, pr.open]
constraints:
  - no_main_write
  - no_merge
  - reserved_files_untouched
  - owner_consumers_and_replay_only
  - no_production_transport
  - no_private_port_run
  - no_private_source_read
  - no_lab_ops_import
  - no_locked_parameter_edit
  - no_dd_constant_edit
  - no_ci_dispatch
  - no_account_or_broker_access
  - no_owner_record_edit
acceptance:
  - tests/ops/test_book_fence_classification.py::test_fresh_working_entry_does_not_block_other_leg_admission
  - tests/ops/test_book_fence_classification.py::test_fresh_working_entry_does_not_block_other_leg_loosening_amend
  - tests/ops/test_book_fence_classification.py::test_fresh_working_entry_on_non_displaced_leg_does_not_block_takeover
  - tests/ops/test_book_fence_classification.py::test_fresh_working_entry_retains_capacity_reservation
  - tests/ops/test_book_fence_classification.py::test_stale_evidence_blocks_admission_loosening_and_takeover
  - tests/ops/test_book_fence_classification.py::test_fresh_working_evidence_after_staleness_reclassifies_known_working
  - tests/ops/test_book_fence_classification.py::test_terminal_resolves_stale_request
  - tests/ops/test_book_fence_classification.py::test_accepted_request_never_evidenced_blocks_from_one_bar
  - tests/ops/test_book_fence_classification.py::test_nonqualifying_evidence_never_makes_request_known_working
  - tests/ops/test_book_fence_classification.py::test_mismatched_identity_symbol_or_remainder_is_not_known_working
  - tests/ops/test_book_fence_classification.py::test_partial_fill_with_fresh_working_remainder_is_known_working
  - tests/ops/test_book_fence_classification.py::test_unknown_dispatch_blocks_immediately
  - tests/ops/test_book_fence_classification.py::test_unknown_dispatch_clears_only_on_accepted_postdating_terminal
  - tests/ops/test_book_fence_classification.py::test_terminal_resolves_only_the_request_it_covers
  - tests/ops/test_book_fence_classification.py::test_takeover_not_blocked_by_non_displaced_order_within_first_bar
  - tests/ops/test_book_fence_classification.py::test_takeover_blocked_by_non_displaced_stale_request
  - tests/ops/test_book_fence_classification.py::test_takeover_requires_displaced_order_terminal
  - tests/ops/test_book_fence_classification.py::test_pre_restart_evidence_never_makes_request_known_working_after_restart
  - tests/ops/test_book_fence_classification.py::test_refreshed_evidence_never_restores_permission_after_incident_halt
  - tests/ops/test_book_fence_classification.py::test_cutoff_cancels_known_working_entry
  - tests/ops/test_book_fence_classification.py::test_deadline_breach_with_known_working_stale_or_unknown_request
  - tests/ops/test_book_fence_classification.py::test_evidence_fresh_just_under_one_bar
  - tests/ops/test_book_fence_classification.py::test_evidence_stale_at_exactly_one_bar
  - tests/ops/test_book_fence_classification.py::test_newer_position_only_read_then_older_full_read_cannot_restore_known_working
  - tests/ops/qualification/test_replay.py::test_orb_base_entry_is_not_cancelled_one_bar_after_admission
  - tests/ops/qualification/test_replay.py::test_orb_base_entry_fills_on_crossing_after_first_bar
  - tests/ops/qualification/test_replay.py::test_orb_base_entry_ends_on_port_session_end_cancel_and_releases_capacity
  - tests/ops/qualification/test_replay.py::test_orb_base_entry_cancelled_at_scheduled_cutoff
  - tests/ops/qualification/test_replay.py::test_one_bar_cancel_still_applies_to_non_orb_base_resting_order
  - tests/ops/qualification/test_replay.py::test_orb_base_entry_lifecycle_matches_emulator_without_schedule_overlay
```

## 0. Read first (report before any code; otherwise `NEEDS_CONTEXT`)

1. `AGENTS.md`. Then [Ruling 7](../programs/2026-09-03-seven-strategy-select-campaign-state.md#ruling-7--orb-lifecycle-l1-reaffirmed-and-the-account-fence-classification-contract-2026-09-27) verbatim, and the [H3 disposition note](../../notes/2026-09-27-orb-fence-ruling6-disposition.md) §1–§5.
2. The owner text as amended 2026-09-27:
   - [rail spec](../../spec/2026-09-12-c1-multi-leg-rail-extension-spec.md): the header callout, the §1 `pending` row marker, S2, S4 and AC-8;
   - [replay spec](../../spec/2026-09-12-tradeify-synchronized-replay-spec.md): the header callout and RC-9.
3. The #519 fence trace at its pinned head: `git show 8c15f18:docs/notes/2026-09-26-account-fence-four-state-trace.md`, §3 (matrix), §4 (producers) and §6.2–§6.4 (repair). Where §6.2's "at most one bar old" differs from Ruling 7(b), **the ruling governs**: evidence is stale when its age at evaluation is one bar period or more (disposition §3).
4. The code, at the dispatch revision:
   - the fence `ops/c1_rail/book_account_owner.py:768-798`;
   - admission `:1605-1612`;
   - attempt journal and dispatch `:1665-1705`;
   - schedule, cutoff and deadline `:1729-1798`;
   - `SyntheticBroker` `:207`, `BrokerFact` `:152-176`, the unknown-fact halt `:2056-2057`;
   - the loosening gate `ops/c1_rail/book_protection_owner.py:484-495`;
   - the takeover fence and quiescence `ops/c1_rail/book_takeover_owner.py:545-559`, `:615-623`;
   - the replay `ops/c1_rail/qualification/replay.py:349-352`, `:404-410`, `:497-543`.
5. The pinned tests:
   - `tests/ops/qualification/test_replay.py:214-223`;
   - `tests/ops/test_book_feedback_journal.py:42-69`;
   - `tests/ops/test_pr409_review4.py:52-126`.

**The report must state:** the dispatch revision; whether each anchor above still matches; the files you expect to change; and whether the evidence ingress for (i) fits the in-scope files (§1). A mismatch is a stop (§7).

## 1. Scope

**In scope:**
- **(F)** The account owner's classification of entry and add requests into states (i)–(iv), per Ruling 7(b) and trace §6.2 as the ruling words it, on the `SyntheticBroker` seam with **synthetic** evidence acquisitions.
- **(F)** The traced consumers, per trace §6.3:
  - admission (`book_account_owner.py:1608`);
  - loosening amends (`book_protection_owner.py:492`);
  - the takeover fence (`book_takeover_owner.py:558`);
  - takeover quiescence (`:621`), which counts unresolved requests ((ii), (iii)) and displaced-leg non-terminal orders only. Implement this with a **new predicate** at `:621`; do not narrow the shared `_unresolved_attempt_rows` helper (`book_account_owner.py:760-766`), because the consumers listed below must keep counting (i).
- **(R)** The qualification replay's one-bar cancel (`replay.py:507-509`), corrected so ORB's base entry follows L1. Scope default per disposition Q3: exempt ORB's base entry only; RC-9's one-bar cancel stays for any other resting entry or add, as RC-9 as amended says. If the coordinator answers Q3 differently before dispatch, it amends this card first.

**Files you may change:**
- `ops/c1_rail/book_account_owner.py`, including its `SyntheticBroker` test seam;
- `ops/c1_rail/book_protection_owner.py`;
- `ops/c1_rail/book_takeover_owner.py`;
- `ops/c1_rail/qualification/replay.py`;
- new `tests/ops/test_book_fence_classification.py`;
- `tests/ops/qualification/test_replay.py`;
- any existing test whose pinned behavior Ruling 7 changes, listed explicitly in the return.

**A change needed anywhere else is a stop (§7).** That includes `book_takeover.py` (`AccountInventory`), `book_synthetic_protection.py`, `book_capacity.py`, `book_migration.py` / `book_migration_schema.py`, the emulator and `c1_signal_daemon/*`.

**Unchanged (trace §6.3).** Cutoff and deadline are re-pinned by case 10; the others are covered by the related suites in §6, not by a new node:
- the same-leg close gate (`:1296-1301`);
- cancel (`:1573-1584`);
- cutoff, flatten and deadline (`:1768-1797`), including the deadline's `_unresolved_attempt_rows` check (`:1793`), which keeps counting (i);
- capacity reservation and release.

**Other consumers, unchanged.** Found by `grep -rn "_ordinary_unknown_orders_db\|_unresolved_attempt_rows" ops/` at `521d8f2`; the #519 trace does not cite them. Their behavior must not change:
- `book_account_owner.py:757`, the `unresolved_attempts` property;
- `book_account_owner.py:810`, `status()`'s `unresolved_attempts` output;
- `book_takeover_owner.py:55`, the takeover plan record's `unresolved=` field;
- `book_takeover_owner.py:547`, `_takeover_pending_db`, already limited to displaced legs.

A known working order still blocks recovery and deadline completion, and is still cancelled at the cutoff.

**Pins that change only as the ruling requires:**
- `tests/ops/test_book_feedback_journal.py:42-55` (the H3 card cites `:41-55`; `:41` is blank) is expected to stay **unchanged**. Its `accepted` case, an order with no evidence fenced at exactly `+15 min`, is consistent with "stale at one bar" (disposition §3). If the repair would change it, stop and return.
- `tests/ops/test_pr409_review4.py:52-126` stays as the state-(ii)/(iii) pin (trace §5).
- `test_replay.py::test_stale_resting_order_cancel_releases_capacity_even_when_flat` (`:214-223`) pins exactly the behavior L1 removes: an ORB entry cancelled at the third bar. It is **replaced** by `test_orb_base_entry_is_not_cancelled_one_bar_after_admission`. The removed node ID is listed in the return as a deliberately changed pin.
- Any other replay test whose outcome depended on the one-bar cancel of an ORB base entry is listed with the reason. It is not silently re-pinned.

## 2. Checkpoint (F): fence classification, tests first

Write the tests first and show that they fail on the unmodified tree, where the ruling changes behavior. Then change the owner and consumers. Each case follows the Ruling 7(b) wording and trace §6.4:

| Case | Ruling words | Test node(s) | Required behavior |
|---|---|---|---|
| 1 | (b1) known working; retain reservation; no block on unrelated admission because old | `test_fresh_working_entry_does_not_block_other_leg_admission`, `…_loosening_amend`, `…_on_non_displaced_leg_does_not_block_takeover`, `…_retains_capacity_reservation` | An entry evidenced fresh on every bar for more than one bar. Another leg's risk-add, loosening amend and non-displaced takeover are admitted; the reservation is held |
| 2 | (b2) stale evidence blocks; (b1) fresh evidence makes a request known working | `test_stale_evidence_blocks_admission_loosening_and_takeover`, `test_fresh_working_evidence_after_staleness_reclassifies_known_working`, `test_terminal_resolves_stale_request` | Blocked from the instant the latest qualifying acquisition is one bar old. A new qualifying acquisition reclassifies the request as (i): assert the classification only (the request leaves `_ordinary_unknown_orders_db`). Do not assert whether the account stays RUNNING; that depends on disposition Q2. Permission is asserted only in case 9. A terminal resolves it |
| 3 | (b2); S1 cut unchanged | `test_accepted_request_never_evidenced_blocks_from_one_bar` | An accepted request with no qualifying evidence is blocked from exactly one bar after preparation. Existing pins stay |
| 4 | "qualifying" (rail spec evidence currency, E1–E3) | `test_nonqualifying_evidence_never_makes_request_known_working`, `test_mismatched_identity_symbol_or_remainder_is_not_known_working` | Parametrize, at least: position-only read; incomplete or unfenced acquisition; `as_of` equal to or before preparation; a read one bar old or older; a read observed later than `MAX_FACT_AGE`; another identity; another symbol; a remainder inconsistent with credited fills. None yields (i). Where E2/E3 require quarantine or a halt that the owner does not implement, assert "not (i)" and record the quarantine/halt as **still owed** |
| 5 | (b1) "working or partially filled" | `test_partial_fill_with_fresh_working_remainder_is_known_working` | A partial fill with a freshly evidenced working remainder is (i) |
| 6 | (b3) blocks immediately; terminal-only; positive lookup held | `test_unknown_dispatch_blocks_immediately`, `test_unknown_dispatch_clears_only_on_accepted_postdating_terminal` | Blocked at once. Parametrize the non-clearing inputs: working evidence for another order; a position-only read; an equal-time terminal; **a positive working lookup of the same order** (held). Only an accepted, postdating terminal clears it |
| 7 | (b4) | `test_terminal_resolves_only_the_request_it_covers` | Two unresolved requests; resolving one does not unblock |
| 8 | (b1)–(b3); S10/K1 displaced scope | `test_takeover_not_blocked_by_non_displaced_order_within_first_bar`, `test_takeover_blocked_by_non_displaced_stale_request`, `test_takeover_requires_displaced_order_terminal` | The account-wide quiescence refusal (`:621-622`), which today counts any `reserved`/`attempted` operation at any age (`book_account_owner.py:760-766`), no longer counts a known working (i) order on a non-displaced leg. A non-displaced stale request blocks. A displaced order must reach a terminal |
| 9 | (b5); S9 | `test_pre_restart_evidence_never_makes_request_known_working_after_restart`, `test_refreshed_evidence_never_restores_permission_after_incident_halt` | Evidence taken before a restart never yields (i) after it, and the owner boots HALTED. After an incident halt, fresh evidence changes classification but never permission. No resume path is added |
| 10 | Unchanged consumers | `test_cutoff_cancels_known_working_entry`, `test_deadline_breach_with_known_working_stale_or_unknown_request` | The cutoff sends the cancel for a request in (i). At D, a request in (i), (ii) or (iii) is a breach |
| 11 | (b2) "stale at one bar … pinning that boundary" | `test_evidence_fresh_just_under_one_bar`, `test_evidence_stale_at_exactly_one_bar` | Age `BAR_PERIOD − 1 µs` is fresh (i); age exactly `BAR_PERIOD` is stale |
| 12 | E1 ordering | `test_newer_position_only_read_then_older_full_read_cannot_restore_known_working` | Replayed or reordered reads cannot restore (i) |

**Evidence ingress.** State (i) needs a synthetic, request-correlated, order-level acquisition input on the owner. Today the owner accepts only `fill` and `terminal` facts; any other kind halts (`:2056-2057`).
- Add the smallest ingress inside the in-scope files, labelled synthetic like `SyntheticBroker`.
- It must never be presented as the T09 producer.
- If it cannot be added without touching an out-of-scope file (for example `AccountInventory` or the schema), stop and return with the proposed file list.

## 3. Checkpoint (R): qualification replay, ORB L1

| Test node | Required behavior |
|---|---|
| `test_orb_base_entry_is_not_cancelled_one_bar_after_admission` | Replaces `:214-223`. An ORB stop entry emitted on the first bar is still pending at the third bar, with its reservation held and no cancel feedback |
| `test_orb_base_entry_fills_on_crossing_after_first_bar` | A crossing on a later bar fills the entry intrabar under emulator rules |
| `test_orb_base_entry_ends_on_port_session_end_cancel_and_releases_capacity` | The adapter's cancel ends it; the reservation is released on the cancel event |
| `test_orb_base_entry_cancelled_at_scheduled_cutoff` | The RC-8 cutoff still cancels it ("The earlier operational cutoff still applies") |
| `test_one_bar_cancel_still_applies_to_non_orb_base_resting_order` | The Q3 default: RC-9's one-bar cancel is unchanged for any other resting entry or add |
| `test_orb_base_entry_lifecycle_matches_emulator_without_schedule_overlay` | **Parity:** on the same synthetic bars with no schedule event inside the span, the replay's ORB base-entry fill or cancel bar equals `TVBrokerEmulator` under `run_adapter` (`tv_broker_emulator.py:638-654`). A mismatch is a stop (§7) |

Record the replay's before/after behavior on these fixtures as the parity record (§6).

## 4. The return must separate these

- **(1) Verified synthetically:**
  - for each case 1–12, the node IDs and the observed classification and consumer behavior;
  - for (R), the replay node IDs and the parity record.

  Each is backed by a launcher `record.json`.
- **(2) Still owed** (not touched here, and not implied by (1)):
  - the real producer of fresh order-level evidence (T09; Gate A A1/A3/A7);
  - route integration;
  - the rev9 halt for ordinary unknowns (B–D packet CC-3; T09/TB-I3);
  - the T09 outcome classifier (the `REJECTED` shortcut and the never-dispatched journal);
  - any E2/E3 quarantine or halt that case 4 found unimplemented.

  **State in words: the fence obligation is not resolved until (2) is accepted.**
- **Open questions carried, not decided:** disposition Q1 (`W`/`AMEND`/evidence-currency boundary), Q2 (stale as a block or a halt), Q4 (**resolved 2026-09-27**: the operator chose a dated §5 addendum entry, now in the rail spec), and positive lookup (held). H4 implements the block only.

## 5. Freeze-inventory effect

Both checkpoints change E1 freeze-inventory components (allocation map row B11: "Any change re-enters the freeze inventory"):
- `ops/c1_rail/qualification/trust_domain.py:146` binds `c1_rail.book_account_owner` as `listener_account_owner`;
- `:158-164` list its runtime dependencies, including `c1_rail.book_protection_owner` and `c1_rail.book_takeover_owner`;
- `:142` binds `c1_rail.qualification.replay` as `replay_kernel`.

The return lists every changed module with its role name, for the coordinator's freeze-inventory record. Both land before the inventory is fixed (addendum §5; CP-6).

## 6. Verification commands

Run through the launcher of your own checkout, and report the command, interpreter, revision, tree state and results. Cite each printed `record.json` and check `status: completed`, exit 0 and `source_stable: true`. Keep the tree unchanged while a recorded check runs.

- `python -I scripts/fp.py doctor` (or `.\fp.ps1 doctor`).
- The new and changed nodes: `python -I scripts/fp.py python -m pytest tests/ops/test_book_fence_classification.py tests/ops/qualification/test_replay.py -q`.
- The related suites. Trace §7 (`8c15f18:docs/notes/2026-09-26-account-fence-four-state-trace.md:238-244`) ran or read every file listed below except `test_book_takeover_phases.py`, and of the two directories only four kernel files under `tests/ops/tb_s3_cases/primitives/` and `tests/ops/qualification/test_replay.py`. H3 adds `test_book_takeover_phases.py` and widens to both whole directories:
  - `tests/ops/test_book_feedback_journal.py`, `tests/ops/test_pr409_review4.py`, `tests/ops/test_pr409_related_cases.py`, `tests/ops/test_pr409_owner_lifecycle.py`;
  - `tests/ops/test_book_close_reconciliation.py`, `tests/ops/test_book_protection_evidence.py`, `tests/ops/test_book_account_owner.py`;
  - `tests/ops/test_book_capacity.py`, `tests/ops/test_book_halt.py`, `tests/ops/test_book_takeover_phases.py`;
  - `tests/ops/tb_s3_cases/`, `tests/ops/qualification/`.
- `python -I scripts/fp.py test-ops` and `python -I scripts/fp.py check`, on the final tree. Disclose any pre-existing gate failure.
- **Linux qualification evidence (S2/S4) is refreshed only as the coordinator directs.** This card grants no `ci.dispatch`; the coordinator dispatches the workflow, or amends the card, per the s2-linux-run discipline. Do not push while a coordinator-dispatched run is in progress.

## 7. Stop conditions (return to the coordinator; do not work around)

- a consumer, not listed in §1, whose behavior the change would alter;
- a needed change outside §1's file list, including the evidence ingress;
- an emulator-parity break in (R);
- the repair would change `test_book_feedback_journal.py:42-55`, or any pin the ruling does not require changing;
- the ORB-base-entry exemption cannot be expressed inside `replay.py` (disposition Q3);
- a test needs a rule Ruling 7 does not decide (Q1, Q2, positive lookup, same-leg "unrelated" admission, same-leg close refusal, loosening during an unresolved close);
- an anchor mismatch at the §0 read.

## 8. Forbidden moves

- Any production transport or route adapter (T09); any `c1_rail_telemetry` evidence path presented as a producer.
- Weakening (iii): no positive-lookup resolution, and no clearing by absence, elapsed time or acknowledgment.
- Adding a halt, a resume path or a same-leg rule (open questions; TB-I3/T09).
- Running, importing or reading any private port or Pine (the synthetic fixtures only); any `lab↔ops` import; any locked parameter or `dd_protection` constant.
- Editing the specifications, the pre-registration, the campaign record, STATE, the handoff set or the disposition note. Contradictions return to the coordinator.
- Any order, account, broker, vendor or network action; any merge; any push to `main`.

## 9. Return boundary

- A `claude/*` (or `codex/*`/`glm/*`) branch and one PR, with the checkpoint (F) and (R) evidence **returned separately** (two sections, or two commits named F and R).
- The four-state status `DONE` / `DONE_WITH_CONCERNS` / `NEEDS_CONTEXT` / `BLOCKED`.
- The §4 separation, the §5 module list, the changed-pin list and the `record.json` paths.
- **The operator merges;** acceptance is the coordinator's, as input to **CP-5**.
- **Recovery:** a branch revert. No shared state is touched.

## 10. Dispatch record

**Dispatched 2026-09-27 on the operator's instruction "dispatch H4 and H5b".**
- **Dispatch revision:** the commit that adds this record, on `claude/clever-wozniak-bx0u95` (PR #520). Read this card there with `git show <revision>:<path>`.
- **Executor:** a Claude Code worker subagent in its own git worktree.
- **Branch:** `claude/h4-fence-classification`, cut from `origin/main` (`5ad04cf`). The owner text it implements is on PR #520 and is read at the dispatch revision; the PR carries code and tests only.
- **Coordinator acceptance of H3's owner text:** `54d6710`.
- **Q3 answer:** the default. Only ORB's base entry is exempt; RC-9's one-bar cancel stays for every other resting entry or add.
- **Linux qualification evidence:** the PR's own path-filtered checks, including "Qualification execution boundary", run automatically. Any further S2/S4 workflow dispatch is the coordinator's.
- **Pre-dispatch read:** `check_handoff_authority.py --all` clean at `54d6710` (2 cards, 0 violations). §0 anchor re-verification is the worker's first act.

**Not granted:**
- freeze, edition file production, replay or E1 dispatch;
- T09 dispatch, gate B–D acceptance;
- CI dispatch, merge, deployment, arming or GO.

A synthetic return never marks the fence obligation resolved.

## Verification of this card

- `python3 scripts/check_handoff_authority.py --all`: after the fix round `2 card(s) with an authority block, 0 violation(s)`, exit 0 (this card and another handoff's concurrently written card).
- Relative-link and anchor check of this card and the other H3 files (scratchpad script, resolving from each file's directory): `bad 0`. `python3 scripts/check_md_relative_links.py` (warn-only) reports no unresolved link in this card. `python3 scripts/check_path_liveness.py`: `OK`, exit 0 (does not cover `docs/**`).
- `grep -rn "_ordinary_unknown_orders_db\|_unresolved_attempt_rows" ops/` at the fix round: the consumers listed in §1.
- **Anchors** were re-read at `521d8f2`:
  - `book_account_owner.py:768-798`, `:1296-1301`, `:1573-1584`, `:1605-1612`, `:1665-1705`, `:1760-1798`, `:2050-2057`;
  - `book_protection_owner.py:484-496`; `book_takeover_owner.py:539-559`, `:615-623`;
  - `replay.py:345-353`, `:402-411`, `:497-545`; `trust_domain.py:142`, `:146`, `:158-164`;
  - `test_replay.py:205-225`, `test_book_feedback_journal.py:38-70`, `test_pr409_review4.py` test list.
- **File checks:** `tests/ops/test_book_fence_classification.py` does not exist at `521d8f2`, so every (F) node is new. The (R) nodes are not in `test_replay.py`'s current test list.
- No test was run for this card.

## Review and fix round (2026-09-27)

Findings are labelled as in the [disposition note's fix round](../../notes/2026-09-27-orb-fence-ruling6-disposition.md#review-and-fix-round-2026-09-27), which records the outcome of each. The ones that changed this card:
- **B-F1 applied:** case 2's node is renamed `test_fresh_working_evidence_after_staleness_reclassifies_known_working` and asserts classification only (Q2 stays open).
- **B-F2 applied:** §1 lists the untraced consumers as unchanged and directs a new predicate at `:621`; the first §7 stop is reworded.
- **B-F5 applied as Q4:** carried in §4.
- **B-F6 applied:** case 8 names the account-wide quiescence refusal; §1 no longer claims new re-pins for the close gate and cancel.
- **A-F5 applied:** `:1768-1797`, `:42-55`, and the related-suite attribution.
- **B-F7 applied:** checker outputs recorded above.

No finding was rejected. The Status line is unchanged: PREPARED, not dispatched.

---

## Coordinator acceptance (2026-09-27)

**ACCEPTED as the H4 dispatch card. Status: READY.** It is dispatchable under §59 Ruling 7's authorization once this commit is on the branch. Before dispatch:
- the coordinator records the dispatch revision, executor and Q3 answer in §10;
- the pre-dispatch read runs.

**Coordinator dispositions:**
- **Q3:** the default is accepted. Only ORB's base entry is exempt.
- **One-bar boundary:** operator-confirmed inclusive (§59 Ruling 7, operator answers). Case 11 pins "age ≥ one bar period is stale".
- **Narrowed stop (cross-handoff critic X-17): an accepted, recorded variance.** The parent H4 card's stop "a consumer the trace missed" is narrowed here to "a consumer, not listed in §1, whose behavior the change would alter". The trace-missed consumers now listed as unchanged are `book_account_owner.py:757`, `:810` and `book_takeover_owner.py:55`, `:547`. Any other consumer the change would alter still stops the work.
- **Q4:** resolved by the §5 addendum entry. It is no longer a dispatch precondition.

**The return must still separate** what is verified synthetically from what is owed: the real producer, route integration and the ordinary-unknown halt (T09/TB-I3). A synthetic result never marks the fence obligation resolved.
