# CC-3 ordinary-unknown halt: synthetic repair evidence (2026-09-29)

**Status:** EVIDENCE, synthetic; executor return is **NEEDS_CONTEXT** (frozen handoff and coordinator dispatch disposition missing). The implementation and test results below are ready for coordinator review. They are not accepted, CC-3 is not RESOLVED, and nothing is committed or pushed. The handoff (`docs/briefs/handoffs/2026-09-29-cc3-ordinary-unknown-halt.md`, PREPARED) is absent from this checkout (main `1ca4233`). A staged, uncommitted copy exists in the `x1-cc3-packets` Codex worktree; that copy supplies no freeze and no dispatch. Implementation began without either.

**Evidence class:** *Synthetic / replay engineering*. Every case uses the existing owner and synthetic route in a disposable `tmp_path` store. No broker, vendor, account, host or notification channel was contacted, and no private input was read.

## 1. The repair

`ops/c1_rail/book_account_owner.py`, `_dispatch_action_locked`, result handling. When the transport result is `unknown` (a returned `unknown` or a caught send exception), the attempt update and `_halt_db(db, "ordinary-unknown:<attempt_id>", "execution", now)` commit in one transaction, inside the existing serializer turn, before any attached fact is consumed and before the result returns. Accepted and rejected results keep the previous ordering. The helper `_settle_attempt_db` carries the attempt update.

Why this placement: a halt after return, or at the next bar, leaves a window in which the serializer is released with the account still `RUNNING`. Here the same serializer turn that recognizes the unknown also commits the halt, so a second sender waits and then meets `intervention_fence`. `_halt_db` is `INSERT OR IGNORE` on the incident id, so a replay adds no second incident or generation.

## 2. Evidence

| Record (`.cache/fp-verification/`) | What | Result |
|---|---|---|
| `20260929T160142Z-0fa5f98ce430` | S1 terminal node with `--runxfail`, unmodified code | failed as the card states: `('RUNNING','NORMAL') != ('HALTED','INTERVENTION')` |
| `20260929T160722Z-63341ffc753d` | new module + rehearsal against **unmodified** `book_account_owner.py` (temporary revert of that one file, restored from a saved patch) | 15 failed, 14 passed: every unknown/halt case fails; the accepted/rejected/refused control passes; `source_stable: true` |
| `20260929T160754Z-99c084756091` | §10 related suite, fixed tree | 1 failed: `test_ambiguous_cutoff_cancel_is_retained_and_deadline_revokes_all_sends` expected a `schedule` incident (see §3) |
| `20260929T161059Z-5ccb92360004` | §10 related suite, fixed tree, after that expectation update and two added cases | 220 passed, `status: completed`, exit 0, `source_stable: true` |
| `20260929T161337Z-1ad15cbc9e66` | `.\fp.ps1 check`, fixed tree, with the docs in place | `completed`, exit 0, `source_stable: true`; three absent-vendor-data WARNs (manifests) as on any public clone |

The base run predates two added cases (`test_halt_storage_failure_stops_remaining_cancel_targets`, `test_protection_unknown_keeps_only_its_own_incident`); those were not run against unmodified code. The protection case is a no-duplicate control and passes on both.

## 3. Cases

- `test_unknown_result_halts_before_return[entry|add|close|cancel]` and `test_send_exception_halts_and_retains_attempt[...]`: durable incident `ordinary-unknown:<attempt_id>` (reason `execution`), HALTED/INTERVENTION, generation +1, bootstrap `ineligible` and invalidated as `incident:ordinary-unknown:<attempt_id>`, attempt retained `UNKNOWN`, reservation retained, later send refused `intervention_fence`.
- `test_terminal_or_fill_after_unknown_never_resumes`: facts attached to the unknown result, and facts observed later, settle the order (exposure `(2, 0)`, no unresolved attempt) while the incident, generation and bootstrap invalidation stay; no resend.
- `test_unknown_halt_survives_restart_and_duplicate_occurrence`: the replayed occurrence returns the stored result with no send and no generation change; two restarts stay HALTED/INTERVENTION with the incident, attempt and reservation retained and no command sent.
- `test_concurrent_dispatch_serializes_behind_unknown_halt`: the second sender is still blocked while the first send is held, then is refused `intervention_fence`; one command total.
- `test_unknown_halts_remaining_cancel_targets`: with three cancel targets, the first becomes unknown and the other two are never sent; all reservations retained.
- `test_halt_storage_failure_suppresses_further_dispatch` and `..._stops_remaining_cancel_targets`: a failure inside the real `_halt_db` (bootstrap invalidation) rolls back the halt **and** the observation; the dispatch raises, no incident row exists, the attempt stays unresolved, later dispatch raises `local send suppression`, remaining cancel targets are not sent, and a fresh boot is HALTED with the attempt retained and nothing resent.
- `test_accepted_rejected_and_refused_do_not_gain_unknown_incident`, `test_protection_unknown_keeps_only_its_own_incident`: no CC-3 incident on accepted, rejected, `zero_size` or `zero_exposure`; a protection unknown keeps only its `protection` incident.
- S1 in `test_attended_incident_rehearsal.py`: XFAIL removed; assertions moved from `unknown_order` to the intervention fence.

**One existing expectation changed.** `test_ambiguous_cutoff_cancel_is_retained_and_deadline_revokes_all_sends` expected the deadline to record a `schedule` incident after an unknown cutoff cancel. The unknown now halts at the cutoff as `execution`, so the later deadline finds INTERVENTION and records nothing more. The no-send and retained-reservation assertions are unchanged.

## 4. Implementation consequence (scheduled exits)

An unknown result on a **scheduled flatten or cutoff cancel** now halts to INTERVENTION, so the deadline flatten is not sent after it. This follows the card's scope (§0.5 A, all paths through `_dispatch_action_locked`) and matches how an unknown protection result already behaves, so after an unknown cutoff cancel or scheduled flatten, later automatic deadline sends are suppressed and operator intervention remains necessary. No deadline exception or resume route was added. Recorded for coordinator review as a consequence of the card, not as a conflict with owner text.

## 5. Not covered, still owed

- The real broker evidence producer and route mapping; actual route recovery.
- Same-session restart design and later-session resume authorization.
- Live notification of the incident.
- Commissioning, arming and any operational GO.
- Crash-cut ambiguity (bytes sent or not) is preserved, not resolved.
- The known Windows acknowledgment-filename failure is not in the §10 modules and did not appear in `check`; it is not repaired or re-tested here (card §5).
- `check_brief.py --type handoff` on the staged, uncommitted card in the `x1-cc3-packets` Codex worktree (read-only, in place): 0 HARD, 0 WARN, well-formed. This is a draft validation of that card's bytes at the time (sha256 `3cda0545...695b1`), not validation of a frozen revision.
