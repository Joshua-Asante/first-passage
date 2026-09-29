# CC-3 ordinary-unknown halt: synthetic repair evidence (2026-09-29)

**Status:** EVIDENCE, synthetic. The repair is on PR [#554](https://github.com/Joshua-Asante/first-passage/pull/554); it is not accepted, CC-3 is not RESOLVED, and the merge is Joshua's. The current disposition is in the card: [§7 executor return](../briefs/handoffs/2026-09-29-cc3-ordinary-unknown-halt.md), [§8 coordinator record](../briefs/handoffs/2026-09-29-cc3-ordinary-unknown-halt.md), §8.1 (amendment 1) and §8.2 (amendment 2). **Historical:** this note first read NEEDS_CONTEXT because the card was absent from the checkout and no freeze or dispatch existed; implementation began without either, which §8 records as a procedural deviation, not repaired by re-running. The card was later frozen at `b77b6f4`.

**Evidence class:** *Synthetic / replay engineering*. Every case uses the existing owner and synthetic route in a disposable `tmp_path` store. No broker, vendor, account, host or notification channel was contacted, and no private input was read.

## 1. The repair

`ops/c1_rail/book_account_owner.py`, `_dispatch_action_locked`, result handling. When the transport result is `unknown` (a returned `unknown` or a caught send exception), one transaction runs `_settle_attempt_db`, then `_halt_db(db, "ordinary-unknown:<attempt_id>", "execution", now)`, then `_observe_locked(fact, ..., db=db)` for every attached fact. All of it sits inside the existing serializer turn and completes before the result returns. Any exception in that transaction sets `_input_send_suppressed` before it re-raises. Accepted and rejected results keep the previous ordering.

`_observe_locked` opens no transaction of its own when it is given `db` (all three `_transaction()` uses are guarded by `db is None`).

**History of the placement.** `b9b72f9` (reviewed at `ec96a0e`) committed the halt in its own transaction *before* the attached facts were journaled. Codex's P1 #1 found that a crash between the two commits would keep the halt and the observation's fact IDs but lose the fact bodies and their capacity effects. Amendment 1 replaced that ordering with the single transaction above.

Why this placement: a halt after return, or at the next bar, leaves a window in which the serializer is released with the account still `RUNNING`. Here the same serializer turn that recognizes the unknown also commits the halt, so a second sender waits and then meets `intervention_fence`. `_halt_db` is `INSERT OR IGNORE` on the incident id, so a replay adds no second incident or generation.

## 2. Evidence

Records are under the checkout's `.cache/fp-verification/`. All show `source_stable: true` and `capture_complete: true` unless a row says otherwise.

| Record | What | Result |
|---|---|---|
| `20260929T160142Z-0fa5f98ce430` | S1 terminal node with `--runxfail`, unmodified code | failed as the card states: `('RUNNING','NORMAL') != ('HALTED','INTERVENTION')` |
| `20260929T160722Z-63341ffc753d` | new module + rehearsal against **unmodified** `book_account_owner.py` (temporary revert of that one file, restored from a saved patch) | 15 failed, 14 passed: every unknown/halt case fails; the accepted/rejected/refused control passes |
| `20260929T160754Z-99c084756091` | §10 related suite, fixed tree | 1 failed: `test_ambiguous_cutoff_cancel_is_retained_and_deadline_revokes_all_sends` expected a `schedule` incident (see §4) |
| `20260929T161059Z-5ccb92360004` | §10 related suite at `b9b72f9` | 220 passed, 0 skipped; completed, exit 0. **Not sufficient for acceptance:** the §10 list omitted the modules in §4 below |
| `20260929T161337Z-1ad15cbc9e66` | `.\fp.ps1 check` with the first draft of this note | completed, exit 0; three absent-vendor-data WARNs (manifests), as on any public clone |
| `20260929T170917Z-44a993effddf` | `.\fp.ps1 check` on the final bytes of the six `b9b72f9` files | completed, exit 0 |
| `20260929T174520Z-5d897db4ba48` | `.\fp.ps1 check` with the card's §7 return | completed, exit 0; reviewed by Codex at `ec96a0e` |
| `20260929T195919Z-96d59d4a2e3d` | new module against `ec96a0e`'s ordering (attached facts after the halt) | 1 failed, 17 passed: `test_attached_fact_failure_rolls_back_halt_and_facts_together` fails, because the halt survives the failed fact observation |
| `20260929T195953Z-6a90667d1c75` | first **full `tests/ops`** run, with the atomic-facts fix | 22 failed, 2920 passed, 18 skipped: the 21 superseded or implicit-unknown nodes in §4, plus `test_qualification_isolation` (timed out in its child at 3,600 s) |
| `FULL_OPS_RECORD` | full `tests/ops`, final head, no other load | `FULL_OPS_RESULT` |
| `FINAL_CHECK_RECORD` | `.\fp.ps1 check` on the final bytes | `FINAL_CHECK_RESULT` |
| `BASELINE_RECORD` | qualification child suite on a clean `main` worktree (`6c6759f`) | `BASELINE_RESULT` |

Coverage gaps, stated plainly: `test_halt_storage_failure_stops_remaining_cancel_targets` and `test_protection_unknown_keeps_only_its_own_incident` were added after the `160722Z` run, so they have no fail-on-base evidence. The protection case is a no-duplicate control. The second new atomic case, `test_unknown_with_attached_fill_commits_capacity_and_halt_together`, passes on both orderings by design.

## 3. Cases

- `test_unknown_result_halts_before_return[entry|add|close|cancel]` and `test_send_exception_halts_and_retains_attempt[...]`: durable incident `ordinary-unknown:<attempt_id>` (reason `execution`), HALTED/INTERVENTION, generation +1, bootstrap `ineligible` and invalidated as `incident:ordinary-unknown:<attempt_id>`, attempt retained `UNKNOWN`, reservation retained, later send refused `intervention_fence`.
- `test_terminal_or_fill_after_unknown_never_resumes`: facts attached to the unknown result, and facts observed later, settle the order (exposure `(2, 0)`, no unresolved attempt) while the incident, generation and bootstrap invalidation stay; no resend.
- `test_unknown_halt_survives_restart_and_duplicate_occurrence`: the replayed occurrence returns the stored result with no send and no generation change; two restarts stay HALTED/INTERVENTION with the incident, attempt and reservation retained and no command sent.
- `test_concurrent_dispatch_serializes_behind_unknown_halt`: the second sender is still blocked while the first send is held, then is refused `intervention_fence`; one command total.
- `test_unknown_halts_remaining_cancel_targets`: with three cancel targets, the first becomes unknown and the other two are never sent; all reservations retained.
- `test_halt_storage_failure_suppresses_further_dispatch` and `..._stops_remaining_cancel_targets`: a failure inside the real `_halt_db` (bootstrap invalidation) rolls back the halt **and** the observation; the dispatch raises, no incident row exists, the attempt stays unresolved, later dispatch raises `local send suppression`, remaining cancel targets are not sent, and a fresh boot is HALTED with the attempt retained and nothing resent.
- `test_attached_fact_failure_rolls_back_halt_and_facts_together`: an unknown result with an attached fill and terminal, where the terminal's capacity append fails. No incident, no `broker_facts` row and no capacity event other than the pre-send reservation survive; the attempt stays `UNKNOWN` with a null observation; later sends are suppressed; a fresh boot is HALTED, retains the attempt and sends nothing.
- `test_unknown_with_attached_fill_commits_capacity_and_halt_together`: after a fresh boot, the incident, both fact bodies, the fill's capacity effect (exposure `(2, 0)`) and the observation listing both facts are all present.
- `test_accepted_rejected_and_refused_do_not_gain_unknown_incident`, `test_protection_unknown_keeps_only_its_own_incident`: no CC-3 incident on accepted, rejected, `zero_size` or `zero_exposure`; a protection unknown keeps only its `protection` incident.

## 4. Per-change table: existing tests

Governing text for every row: [halt/resume §2](../spec/2026-09-14-tb-s3-halt-resume-contract.md) and [incident ADR §A11.2](../adr/2026-09-17-bounded-platform-protection-incident-contract.md): an unknown outcome is an incident, and no automatic send resumes after it in the session. Every no-send, reservation, reconciliation, late-fill and restart assertion in these tests is kept.

**Explicit-unknown tests (authority expectation only; amendment 1).**

| Node | Old expectation | New expectation |
|---|---|---|
| `test_attended_incident_rehearsal.py::test_lost_entry_response_blocks_risk_add_at_once` | risk-add refused `unknown_order` | refused `intervention_fence`; incident `ordinary-unknown:<attempt>` asserted |
| `test_attended_incident_rehearsal.py::test_lost_entry_response_terminal_does_not_restart_automation_in_session` | strict XFAIL (CC-3 defect pinned) | passes: still HALTED/INTERVENTION after the terminal, generation unchanged, activation refused |
| `test_book_account_owner.py::test_ambiguous_cutoff_cancel_is_retained_and_deadline_revokes_all_sends` | the deadline records a later `schedule` incident | one `execution` incident at the cutoff; the deadline records nothing more |
| `test_pr409_related_cases.py::test_close_refuses_live_entry_remainder_until_terminal[unknown-exit-False]`, `[unknown-flat-False]`, `[unknown-exit-True]` | close refused `entry_remainder_pending`; after the late facts a new close is admitted | close refused `intervention_fence`; late facts reconcile (exposure `(2, 0)`); a new close is still refused; commands stay `['entry', 'cancel']` |
| `test_book_close_reconciliation.py::test_close_demands_queue_per_symbol_without_reserving_or_sending_twice[unknown]` | second close queued `close_pending`; `resume_closes` sends it after the terminal | second close refused `intervention_fence`; `resume_closes` returns nothing; two commands only |
| `test_pr409_review4.py::test_unresolved_ordinary_order_blocks_other_leg_until_postdating_terminal[unknown-1]` | other leg refused `unknown_order`; after the terminal a send is `accepted` | refused `intervention_fence`; the terminal reconciles (exposure `(0, 0)`); the later send is refused, not sent |
| `test_pr409_review4.py::test_unknown_order_equal_time_terminal_does_not_clear_and_restart_retains_attempt` | refused `unknown_order` | refused `intervention_fence`; restart and no-resend assertions unchanged |
| `test_book_fence_classification.py::test_unknown_dispatch_blocks_immediately` | refused `unknown_order` | refused `intervention_fence`; HALTED/INTERVENTION asserted; the fence classification `('base',)` is unchanged |
| `test_book_fence_classification.py::test_unknown_dispatch_clears_only_on_accepted_postdating_terminal[other_order_working, position_only, equal_time_terminal, positive_lookup_same_order]` | refused `unknown_order`; after an accepted terminal a send is `accepted` | refused `intervention_fence`; the classification still clears to `()`; the later send is refused and no command is added |
| `test_book_fence_classification.py::test_terminal_resolves_only_the_request_it_covers` | `still-blocked` refused `unknown_order`; after both terminals a send is `accepted` | refused `intervention_fence`; the classification assertions are unchanged; no command is added |
| `test_book_fence_classification.py::test_deadline_breach_with_known_working_stale_or_unknown_request[unknown]` | cutoff sends a `cancel`; the deadline records `own-flat-deadline` | no automatic cancel (the account halted at dispatch); the only incident is `ordinary-unknown:<attempt>`; the request stays classified `unknown` |

**Implicit-unknown fixtures made explicit (amendment 2).** Cause for every row: *implicit unknown via empty queue; fixture made explicit*. `SyntheticBroker.send` returns `BrokerResult("unknown")` when its queue is empty, so these tests hit an unknown they never meant to test. The default is unchanged.

| Node | Change |
|---|---|
| `test_book_takeover_phases.py::test_producer_cancel_removes_remainder_and_retains_late_fill` | the route is built with two `accepted` results (entry, cancel) |
| `test_pr409_owner_lifecycle.py::test_scheduled_close_survives_ticks_and_partial_terminal` | two `accepted` results queued (scheduled flatten and its remainder) |
| `test_pr409_owner_lifecycle.py::test_invalid_cancel_target_never_sends[other-leg]` | `accepted` queued for the setup entry |
| `test_pr409_owner_lifecycle.py::test_invalid_cancel_target_never_sends[close]` | `accepted` queued for the setup exit |
| `test_pr409_owner_lifecycle.py::test_scheduled_flatten_handles_late_entry_fill` | three `accepted` results (entry, scheduled cancel, final flatten) |
| `test_pr409_owner_lifecycle.py::test_async_cancel_terminal_resolves_control_attempt[unknown]` | entry `accepted`, cancel `unknown` (before: both unknown, so the cancel was never sent); authority after the deadline is `INTERVENTION` (was `SCHEDULED_EXIT`); the unresolved-attempt and reconciliation assertions are unchanged |
| `test_pr409_review3.py::test_cutoff_retires_takeover_before_displaced_terminal` | two `accepted` results (orb entry, cutoff cancel) |
| `test_pr409_review2.py::test_definitive_rejection_releases_only_its_own_reservation[cancel]` | `accepted` queued for the setup entry |

## 5. Implementation consequence (scheduled exits)

An unknown result on a **scheduled flatten or cutoff cancel** now halts to INTERVENTION, so the deadline flatten is not sent after it. This follows the card's scope (§0.5 A, all paths through `_dispatch_action_locked`) and matches how an unknown protection result already behaves, so after an unknown cutoff cancel or scheduled flatten, later automatic deadline sends are suppressed and operator intervention remains necessary. No deadline exception or resume route was added. Recorded for coordinator review as a consequence of the card, not as a conflict with owner text.

## 6. Not covered, still owed

- The real broker evidence producer and route mapping; actual route recovery.
- Same-session restart design and later-session resume authorization.
- Live notification of the incident.
- Commissioning, arming and any operational GO.
- Crash-cut ambiguity (bytes sent or not) is preserved, not resolved.
- The known Windows acknowledgment-filename failure is not in the modules run and did not appear in `check`; it is not repaired or re-tested here (card §5).
- Independent Linux execution evidence: every record above is a Windows launcher run (Python 3.13.2).
- `check_brief.py --type handoff` and `check_handoff_authority.py` on the frozen card, and again after §8.2: 0 HARD, 0 WARN, 0 violations.
