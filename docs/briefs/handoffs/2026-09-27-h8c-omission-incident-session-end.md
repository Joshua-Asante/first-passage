# H8(c) — Omitted required slot ends the session: bounded test card — worker card

**Status:** PREPARED 2026-09-27 by the coordinator on accepting [H8 step (b)](../../notes/2026-09-27-h8b-feed-gap-classification.md#coordinator-acceptance-2026-09-27). **Not dispatched.** **READY ON** two events:
- the PR carrying this card is accepted and merged;
- [PR #521](https://github.com/Joshua-Asante/first-passage/pull/521) (H5 step (b)) is merged, because its test module is this card's regression base. #521 is accepted **partially**, under its §7 (B) variance. It keeps one strict XFAIL for CC-3 (an ordinary unknown outcome raises no halt), and a locally reproduced environmental `test-ops` failure is disclosed. Using it as a regression base does not imply complete incident-contract compliance.

The two PRs may merge in either order; both must land before dispatch. At dispatch the coordinator records the exact resulting `origin/main` revision in §9 and reruns the pre-dispatch checks against it.

At dispatch the coordinator records the dispatch revision in §9 and runs the pre-dispatch read ([surface-allocation ADR](../../adr/2026-07-14-cc-cursor-surface-allocation.md#decision), *Action classes and the authority block*).

**Parent:** [staged acceptance handoff set, card H8](2026-09-27-staged-acceptance-handoffs.md#h8--feed-provider-neutral-preparation). The parent file carries no authority block, so it bounds nothing beyond this card's own seat checks.

**Authority.** The operator ruled on 2026-09-27, recorded in the [halt/resume contract §4.1](../../spec/2026-09-14-tb-s3-halt-resume-contract.md#41-amendment-2026-09-27-incident-versus-correctly-handled-refusal), *Qualifications*, "An omitted required slot is an incident": "an omitted required slot — including an uncaptured early close — is an incident that ends automation for the session (armed commissioning and first attended release), whichever detector reports it (feed-silence, barrier-expired, bar-sequence, invalid-bar-time)" and "Scheduled closures and valid refusals stay non-incidents." This card verifies that the existing owners behave that way. It grants nothing its dispatcher lacks.

```yaml authority
seat: worker
parent: docs/briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push, pr.open]
constraints:
  - no_main_write
  - no_merge
  - tests_and_evidence_note_only
  - no_production_code_change
  - no_new_interface_for_testing
  - no_rail_deploy
  - no_rail_arm
  - no_account_traffic
  - no_broker_or_vendor_contact
  - no_external_send
  - disposable_state_only
  - no_private_source_read
  - no_lab_ops_import
  - no_ci_dispatch
  - no_owner_record_edit
acceptance:
  - tests/ops/test_feed_omission_session_end.py::test_single_leg_omission_under_loop_records_feed_silence_then_barrier_expired
  - tests/ops/test_feed_omission_session_end.py::test_omission_reaching_runtime_before_expiry_records_bar_sequence
  - tests/ops/test_feed_omission_session_end.py::test_all_legs_silent_uncaptured_early_close_records_feed_silence
  - tests/ops/test_feed_omission_session_end.py::test_late_bar_invalid_bar_time_regression_ends_session
  - tests/ops/test_feed_omission_session_end.py::test_recovered_bars_after_omission_halt_dispatch_nothing
  - tests/ops/test_feed_omission_session_end.py::test_repeated_bootstrap_activation_refused_after_omission_halt
  - tests/ops/test_feed_omission_session_end.py::test_reopened_journal_after_omission_halt_stays_halted
  - tests/ops/test_feed_omission_session_end.py::test_repeated_incident_id_preserves_identity_and_generation
  - tests/ops/test_feed_omission_session_end.py::test_distinct_detectors_neither_restore_authority_nor_drop_obligations
  - tests/ops/test_feed_omission_session_end.py::test_recovery_and_evidence_entry_points_remain_available_after_omission_halt
  - tests/ops/test_feed_omission_session_end.py::test_scheduled_cutoff_without_omission_records_no_incident
```

## 0. Read first (report before any test code; otherwise `NEEDS_CONTEXT`)

- `AGENTS.md`.
- Halt/resume contract §1–§4.1 and §7, including the 2026-09-27 omitted-slot entry under §4.1 *Qualifications* and §4.1 *Implementation status*.
- Incident ADR §A11.2, with its clarifications.
- The [H8(b) note](../../notes/2026-09-27-h8b-feed-gap-classification.md): §5 (the conditions and the synthetic trace) and *Coordinator acceptance*.
- Owners, at the dispatch revision:
  - `ops/c1_signal_daemon/book_runtime.py`: `on_completed_bar`, `expire_barrier` and `recover`;
  - `ops/c1_signal_daemon/book_evaluate_loop.py`;
  - `ops/c1_rail/book_account_owner.py`: `halt`, `_halt_db`, `check_source_silence`, `expire_partial_barrier`, `boot`, `advance_schedule` and `resume_closes`;
  - `ops/c1_rail/book_bootstrap.py`: `_activate_bootstrap` and its guards.
- Tests: `tests/ops/test_four_leg_runtime.py`, `tests/ops/test_attended_incident_rehearsal.py` (from #521), `tests/ops/test_book_bootstrap_migration.py` and `tests/ops/test_book_account_owner.py`. Reuse their fixtures; add no fixture module.

Report the line anchors of each owner path you rely on. If any path named above does not exist at the dispatch revision, stop (§6).

## 1. Scope

**In scope.**
- One new test module, `tests/ops/test_feed_omission_session_end.py`.
- One evidence note, `docs/notes/<dispatch-date>-h8c-omission-incident-evidence.md`.
- A return section appended to this card.

**Out of scope.**
- Any production code change.
- Any edit to an existing test.
- Any new interface. In particular, **do not create a "resume request" API, endpoint or helper merely to test its rejection.** None exists (halt/resume §4.1 *Implementation status*). The test drives only the real entry points in §2.
- Any later-session re-arming design. That is an outstanding obligation for TB-I3 and the resume decision (halt/resume §4). This card records it and does not build it.

**What the bootstrap evidence means.** `book_bootstrap.py` is the offline one-use bootstrap. A refused re-activation shows how **the current owner implementation** behaves. It is not proof of a complete production re-arming policy. The evidence note must say so.

## 2. Cases (the acceptance nodes)

**Setup for every case:**
- a synthetic session binding and synthetic adapters and broker, as in `test_four_leg_runtime.py`;
- the four legs deliver on time;
- the evaluate loop is stepped at a cadence of 30 s or less, unless the case says otherwise;
- "ends the session" means `permission == HALTED`, `authority == INTERVENTION`, and no broker command dispatched after the halt.

| Node | Drive | Must show |
|---|---|---|
| `…records_feed_silence_then_barrier_expired` | One leg omits one boundary, then several. The other three deliver. Run through `FourLegEvaluateLoop.step` | The first incident is `feed-silence` and `barrier-expired` follows in the same step, at the first step strictly after the gap boundary + 15 m 30 s (H8(b) §5). The session ends. The count of omitted slots does not change the result |
| `…before_expiry_records_bar_sequence` | The same omission. The later boundary reaches `FourLegRuntime.on_completed_bar` with no `expire_barrier` call between | `bar-sequence`. The session ends |
| `…uncaptured_early_close_records_feed_silence` | All four legs stop delivering mid-session on a regular permitted row. This models an early close no calendar source recorded | `feed-silence`, with no partial barrier. The session ends. The scheduled-cutoff path is **not** taken |
| `…late_bar_invalid_bar_time_regression…` | **Not an omission.** A bar handled after bar_open + 15 m 30 s, for example because the loop cadence is slower than `BAR_SLACK` | `invalid-bar-time`. The session ends. This pins the already-ruled late-bar case as a regression, not a new omission detector |
| `…recovered_bars_…dispatch_nothing` | After an omission halt, all four legs resume on time. Drive the loop, **and** call `on_completed_bar` directly | Under the loop, `step` returns without dispatch. A direct call may record partials or barriers, but dispatches nothing. The authority stays INTERVENTION |
| `…repeated_bootstrap_activation_refused…` | After an omission halt in the same session, attempt the real activation path again (`activate_synthetic` / `_activate_bootstrap`). **Every other precondition must hold at the attempt:** the time is inside the session's risk-add window, the binding is within `as_of`/`valid_until` and `max_evidence_age`, and the settlement binding validates. Assert these explicitly before the attempt | The activation is refused **because of the incident**: the error is `fresh bootstrap entitlement required`, the persisted bootstrap is `ineligible`, and its invalidation is `incident:<the omission incident id>`. A refusal for any other reason (a stale binding, outside the window, a settlement refusal, storage suppression) does **not** satisfy the node. Permission stays HALTED |
| `…reopened_journal_…stays_halted` | After an omission halt, reopen the retained journal with `BookAccountOwner.boot` on the same path and a binding that is otherwise valid and fresh (the same preconditions as the previous row, asserted explicitly). Then attempt activation | The owner boots HALTED/INTERVENTION with its incident rows retained. The activation is refused with `fresh bootstrap entitlement required`. The persisted invalidation still names the original `incident:<id>`, because a restart does not overwrite it. A refusal for any other reason does not satisfy the node |
| `…repeated_incident_id_preserves_identity_and_generation` | Report the same incident id again. Include both paths: `check_source_silence` at a later `now` with an unchanged anchor, and `halt()` with the same id and reason | Exactly one row for that id, with its original `at` and generation, and no generation bump. **Also record what `halt()` does when the same id arrives with a different `at`.** The owner is expected to raise "conflicting incident identity". Pin whatever it actually does, provided the authority stays INTERVENTION |
| `…distinct_detectors_neither_restore_…nor_drop_obligations` | One omission produces `feed-silence` and `barrier-expired` as **separate** records | Separate records are allowed; the ruling requires no deduplication. Neither record restores authority. Recovery obligations, such as the HALT events on existing takeover plans and retained partial or protection state, are neither lost nor cleared by the second record |
| `…recovery_and_evidence_entry_points_remain_available…` | After an omission halt, deliver **valid, causally appropriate** evidence through the existing entry points. Examples: close feedback and broker facts (via the listener's book-fact handler) for orders or positions that existed before the halt, and status reads | **Firm condition:** each item is recorded or accepted, and none restarts automation or dispatches. If an item is refused **because of the incident state**, the node fails. Return the failing test with its evidence and leave this criterion **unaccepted** (§6). Do not change production code. An item refused for an unrelated, valid reason (for example an unknown order identity) is not a pass: replace it with valid evidence |
| `…scheduled_cutoff_without_omission_records_no_incident` | All four legs deliver on time up to the scheduled risk-add cutoff | SCHEDULED_EXIT with **no** incident row. A scheduled closure stays a non-incident |

**Regression runs, not new nodes.** Run the H5(b) module unchanged, including its correctly-handled-refusal and incomplete-barrier-before-expiry nodes, and `test_four_leg_runtime.py`.

## 3. Evidence retained

The evidence note records:
- the command, interpreter and revision;
- the launcher verification record path, with `status`, `verification_exit_code` and `source_stable`;
- the per-node result;
- the incident ids, reasons and generations observed in each case;
- the `halt()` behavior for the same id with a different `at`;
- any entry point that refused evidence after a feed incident;
- the qualification of the bootstrap evidence (§1);
- the outstanding later-session obligation.

## 4. Verification commands

From the worktree root:
- `.\fp.ps1 doctor`
- `.\fp.ps1 python -m pytest tests/ops/test_feed_omission_session_end.py tests/ops/test_attended_incident_rehearsal.py tests/ops/test_four_leg_runtime.py -q`
- `.\fp.ps1 check`

Cite each printed `record.json`. A run counts only when `status: completed`, the exit code is 0 and the source is stable. Disclose any failure that pre-exists this change.

## 5. Synthetic versus owed

This card establishes owner-level behavior, synthetically. It does not establish:
- live feed behavior or arrival timing;
- a production re-arming policy;
- a resume mechanism;
- the cause of the H8(b) MGC omission.

## 6. Stop conditions (return to the coordinator; do not work around)

- **A case can pass only by changing production code.** Return the failing test with its evidence. Do not mark it `xfail` unless the coordinator records a variance.
- **A case shows authority restored, a dispatch after the halt, or a recovery obligation lost.** Stop. This is a defect for TB-I3.
- **Valid, causally appropriate evidence is refused because of the incident state** (the recovery/evidence node). Return the failing test. That criterion stays unaccepted, and the other nodes may still be returned. Production code is not changed.
- **A case can be driven only through an interface that does not exist.** Return it as a contract question. Do not build the interface.
- **A named owner path, or the #521 module, is absent** at the dispatch revision.
- **Behavior contradicts the ruling in a way the ruling's text does not settle,** for example a detector that ends the session in one context but not another.

## 7. Forbidden moves

- Editing production code, existing tests, owner specifications or this card's parent.
- Inventing a resume, operator or HTTP interface.
- Reading private sources or the book's Pine or ports.
- Any deploy, arm, account traffic, CI dispatch or external send.

## 8. Return boundary

Status `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED` or `NEEDS_CONTEXT`. The return holds:
- a `claude/*` branch cut from the frozen dispatch revision;
- one PR holding only the §1 files;
- a per-node table;
- the verification records.

The operator merges. The coordinator keeps acceptance.

## 9. Dispatch record

**Dispatched 2026-09-27 on the operator's instruction "merge both as recommended, then dispatch H8(c) from the main revision".**
- **Dispatch revision:** `origin/main` `08196100b5b0b4f0337c3f5585c39ab4e121da24`, the merge of #521. It already contains #528, merged at `c1d2532`. Both READY ON events hold.
- **#521's final head:** `b4648f7`. Its last commit is an operator docstring qualification: S1 stays a strict XFAIL under CC-3, and acceptance is partial. The test logic is unchanged from the accepted `32e0863` and `c86e940`.
- **Branch:** `claude/h8c-omission-incident-tests`, cut from the dispatch revision. It is checked out in the coordinating session's worktree (`.claude/worktrees/bracket-timing-convention-build-43a332`), because the session's worktree-isolation hook confines writes to that worktree. The coordinator makes no edits while the worker runs. This record is the branch's first commit, made by the coordinator.
- **Executor:** a Claude Code worker subagent in that worktree. It is not routed to GLM: the work is incident-contract work, and the card forbids external sends.
- **Pre-dispatch read (coordinator, at the dispatch revision):**
  - `check_handoff_authority.py --all`: 3 cards, 0 violations.
  - This card is byte-identical to the reviewed `00f6db1`.
  - Every §0 owner path and test module exists: `boot` `:318`, `check_source_silence` `:847`, `expire_partial_barrier` `:916`, `activate_synthetic` `:1099` and `halt` `:1112` in `book_account_owner.py`; `_activate_bootstrap` `book_bootstrap.py:106`; `handle_book_fact` `c1_rail_listener.py:125`.
  - `tests/ops/test_feed_omission_session_end.py` does not exist yet.
  - `.p.ps1 doctor` is OK (ops-env Python 3.13.2).
- **Pre-existing regression-base failure (disclose; do not fix).** At the dispatch revision, on Windows, `pytest tests/ops/test_attended_incident_rehearsal.py tests/ops/test_four_leg_runtime.py` gave 34 passed, 3 skipped, 1 xfailed and **1 failed**. The launcher record was `status: failed`.
  - The failing node is `test_attended_incident_rehearsal.py::test_missed_acknowledgment_never_changes_halt_or_permission`.
  - `FileAckNotifier.acknowledge` (`c1_rail_telemetry.py:220`) writes a filename that contains `:`, which Windows rejects (`OSError: [Errno 22]`). The node passes on Linux CI.
  - This is outside H8(c)'s scope and routed separately. The worker reports it as pre-existing and must not treat it as caused by or fixed in this card. Every other regression node must pass.

**Not granted:** a production code change, a rail deploy or arm, account traffic, an order, CI dispatch, a merge, deployment, GO or later-release policy.
