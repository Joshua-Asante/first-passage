# H8(c) omitted required slot ends the session: evidence (2026-09-27)

**Status:** EVIDENCE, synthetic. Worker return for [handoff H8 step (c)](../briefs/handoffs/2026-09-27-h8c-omission-incident-session-end.md), dispatched at `origin/main` `08196100` (§9 of the card). **Acceptance is the coordinator's.** The operator merges.

**Evidence class:** *Synthetic / replay engineering*. Every case runs the existing owners (`FourLegEvaluateLoop`, `FourLegRuntime`, `BookAccountOwner`, the listener's `handle_book_fact` and `handle_book_protection`) in a disposable `tmp_path` store. The account, session, clock, adapters, broker, identifiers and prices are synthetic. Nothing was armed or deployed. No broker, vendor or account was contacted, and nothing was sent to an external channel. No production code changed, and no interface was added.

**Tests:** `tests/ops/test_feed_omission_session_end.py`, with the card's 11 acceptance nodes (16 cases with parameters). The ruling verified is the omitted-slot entry of [halt/resume §4.1](../spec/2026-09-14-tb-s3-halt-resume-contract.md#41-amendment-2026-09-27-incident-versus-correctly-handled-refusal), *Qualifications*, under [incident ADR §A11.2](../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a112--operator-ruling-no-same-session-restart-of-automation-after-an-incident-2026-09-27).

## 0. Owner anchors relied on (read at `08196100`; `ops/` unchanged at the branch head)

| Owner | Anchors |
|---|---|
| `ops/c1_signal_daemon/book_runtime.py` | `observe_fact` `:292`; `on_completed_bar` `:332` → `_on_completed_bar` `:336`; late/out-of-session halt `invalid-bar-time` `:350–:353`; first-bar and overtaking `bar-sequence` `:371–:373`, `:376–:381`; `expire_barrier` `:477` (strict threshold `:483`); `recover` `:487–:488` |
| `ops/c1_signal_daemon/book_evaluate_loop.py` | `step` `:29`; silence check `:33`; expiry before polling `:35–:36`; INTERVENTION returns `:37–:38`, `:47–:48`; polling `:49–:55`; expiry after polling `:56–:57` |
| `ops/c1_rail/book_account_owner.py` | `boot` `:318` → `_boot_locked` `:324` (restart invalidation `:387`, generation bump `:388–:389`); `_validate_settlement_binding` `:632`; `check_source_silence` `:847` (INTERVENTION guard `:854–:855`, anchor `:859–:863`, halt `:864–:866`); `expire_partial_barrier` `:916` (halt `:924`); `activate_synthetic` `:1099`; `halt` `:1112` (identity conflict `:1120–:1123`); `resume_closes` `:1252` (INTERVENTION `:1257–:1258`); `advance_schedule` `:1725` → `_advance_schedule_locked` `:1729` (INTERVENTION `:1743–:1744`, cutoff transition `:1746–:1749`); `_halt_db` `:1868` (insert `:1871`, generation `:1873–:1874`, bootstrap invalidation `:1876`, takeover HALT events `:1877–:1879`); `observe` `:1884` |
| `ops/c1_rail/book_bootstrap.py` | `_invalidate_bootstrap_db` `:98` (first reason kept `:102–:103`); `_activate_bootstrap` `:106` (suppression `:115–:116`, settlement `:117–:119`, window `:121–:122`, binding freshness `:123–:125`, entitlement `:127–:131`) |
| `ops/c1_rail/c1_rail_listener.py` | `handle_book_protection` `:99`; `handle_book_fact` `:125` |
| `ops/c1_rail/book_takeover_owner.py` | `_takeover_event_db` `:32` |
| `ops/c1_signal_daemon/book_protocol.py` | `BAR_PERIOD` `:39`, `BAR_SLACK` `:40` |

Every path named in card §0 exists at the dispatch revision, and so does the #521 module.

## 1. Setup

- **Session:** the `test_four_leg_runtime.py` binding, `tradeify-account-day:2026-09-15`. It opens at `NOW` = 2026-09-15T14:00Z, the risk-add cutoff is 15:00Z and it closes at 16:00Z. Slot bk opens at `NOW + k × 15 min`. The binding's `valid_until` and `max_evidence_age` are widened to the risk-add cutoff, so an in-window activation attempt meets every precondition except the entitlement.
- **Delivery:** each leg's completed bar arrives 2 s after it closes. The loop is stepped every 15 s or 29 s, both within the 30 s slack. The omitting leg is MGC (`vanguard_mgc`).
- **Broker and adapters:** `BootstrapBroker` (synthetic), with `test_four_leg_runtime`'s adapters or a scripted subclass of its `Adapter`.
- **"Ends the session":** `permission == HALTED`, `authority == INTERVENTION`, and no broker command after the halt.

## 2. Per-node result

States are (permission, authority, generation). Generation 1 is the activated session. `S` is the session ID, `b1` = 14:15Z, `b2` = 14:30Z and `b3` = 14:45Z.

| Node | Result | What it asserts | Incidents observed (id; reason; generation at insert) |
|---|---|---|---|
| `test_single_leg_omission_under_loop_records_feed_silence_then_barrier_expired` (1 or 6 omitted slots × 15 s or 29 s cadence) | **PASS** (4/4) | Halt at the first step strictly after b2 + 15 m 30 s: 14:45:45Z at 15 s, 14:45:55Z at 29 s. Both incidents are recorded in that one step. The six-slot run continues past b3's own threshold with no further incident. Final state HALTED, INTERVENTION, 3. Aegis's b0 entry is the only broker command, sent before the halt | `feed-silence:S:b1`; feed; 1. `barrier-expired:b2`; barrier; 2 |
| `test_omission_reaching_runtime_before_expiry_records_bar_sequence` (1 or 6) | **PASS** (2/2) | Direct `on_completed_bar`, with no expiry call. The first b3 bar at 15:00:02Z raises `noncontiguous bar boundary`. HALTED, INTERVENTION, 2. No command after the halt | `bar-sequence:b3`; barrier; 1 |
| `test_all_legs_silent_uncaptured_early_close_records_feed_silence` | **PASS** | All four legs stop after b1. Halt at 14:45:45Z, with no partial barrier. Stepping through the 15:00Z cutoff to 15:01Z leaves HALTED, INTERVENTION, 2: no SCHEDULED_EXIT, no generation bump and no scheduled cancel of the still-active Aegis entry | `feed-silence:S:b1`; feed; 1 (only) |
| `test_late_bar_invalid_bar_time_regression_ends_session` | **PASS** | Not an omission; every leg delivers. With a 60 s cadence, b0 is handled at 14:16:00Z, past b0 + 15 m 30 s, and the step raises. HALTED, INTERVENTION, 2. No command was ever sent, and later steps return `None` | `invalid-bar-time:b0`; barrier; 1 |
| `test_recovered_bars_after_omission_halt_dispatch_nothing` | **PASS** | After the omission halt all four legs deliver b3 and b4 on time. The loop's `step` returns `None` and never polls them. Direct delivery of b3 raises `noncontiguous` for each leg, records one more row, and prepares no partial, barrier or adapter evaluation (ORB's adapter was scripted to emit an entry on b3 and b4). No broker command | Omission rows as node 1, plus `bar-sequence:b3`; barrier; 3. Final generation 4 |
| `test_repeated_bootstrap_activation_refused_after_omission_halt` | **PASS** | At 14:46:00Z, asserted first: inside the risk-add window; `as_of ≤ t < valid_until` and age ≤ `max_evidence_age`; no send suppression; `_validate_settlement_binding` returns `None` and writes nothing. Then `activate_synthetic` raises exactly `fresh bootstrap entitlement required`. Bootstrap `ineligible`, invalidation `incident:feed-silence:S:b1`. Generation and boot ID unchanged | Omission rows as node 1 |
| `test_reopened_journal_after_omission_halt_stays_halted` | **PASS** | `BookAccountOwner.boot` on the same path and binding: HALTED, INTERVENTION, generation 3 → 4, new boot ID, incident rows identical. The invalidation stays `incident:feed-silence:S:b1`, not `restart`. The same preconditions are asserted, and the refusal is the same exact message | Omission rows as node 1 |
| `test_repeated_incident_id_preserves_identity_and_generation` | **PASS** | (1) `check_source_silence` 5 min later, anchor b1 unchanged: no change. (2) `halt()` with the same id, reason and `at`: one row, no generation bump. (3) `halt()` with the same id and `at` + 1 s: raises `conflicting incident identity`, writes nothing, stays INTERVENTION. After all three: rows, state (HALTED, INTERVENTION, 3) and bootstrap invalidation unchanged | Omission rows as node 1 |
| `test_distinct_detectors_neither_restore_authority_nor_drop_obligations` (`takeover`, `partial_fill`) | **PASS** (2/2) | The two records are separate rows. HALTED, INTERVENTION, 3 after both, and the next step dispatches nothing. Exposures, unresolved attempts, operations, protection owners, pending feedback and takeover plans are identical just before and just after the halt step. *takeover:* a filled ORB lot (1, 0) and Aegis's takeover plan at PLAN; the journal gains HALT events `entry:aegis_6j:1` (feed-silence) and `:2` (barrier-expired), and the PLAN event is kept. *partial_fill:* a Striker entry with 1 filled and the remainder working; one unresolved attempt is retained | Omission rows as node 1, in both variants |
| `test_recovery_and_evidence_entry_points_remain_available_after_omission_halt` | **PASS** (firm condition met) | Pre-halt: a working Striker entry, a filled ORB lot and a working ORB exit of that lot. After the halt each item is **recorded**: (1) the Striker fill and filled terminal via `handle_book_fact` (the adapter receives the fill); (2) the ORB exit's fill and filled terminal via `handle_book_fact` (the adapter receives the close feedback); (3) a complete protection read of both legs via `handle_book_protection`, retained as kind `snapshot`; (4) `status()`, `observable_accounting()` and `observable_state()` reads, which are pure. Exposures then show Striker (q, 0) and ORB (0, 0); all three operations are `terminal`; no unresolved attempts or pending feedback. Rows, state (HALTED, INTERVENTION, 3) and the broker command count are unchanged throughout, and the loop still returns `None` | Omission rows as node 1; no new row |
| `test_scheduled_cutoff_without_omission_records_no_incident` | **PASS** | Every leg delivers b0–b3 on time. At the 15:00Z cutoff: HALTED, SCHEDULED_EXIT, 2, with **no incident row** and the bootstrap invalidation still `None`. The scheduled path ran: its own `cancel` of Aegis's resting entry, under SCHEDULED_EXIT, producer `schedule` | none |

**`halt()` with the same id and a different `at`:** it raises `AccountOwnerError("conflicting incident identity")` (`book_account_owner.py:1122–:1123`) before any write. The row keeps its original `at` and generation, and the authority stays INTERVENTION.

**Evidence refused after the feed incident:** none. Every valid, causally appropriate item offered in the evidence node was recorded or accepted, and none restarted automation or dispatched.

## 3. Observations (no defect claimed)

- **A second record is possible after the halt.** In the recovered-bars node, direct runtime delivery of b3 adds `bar-sequence:b3` (a third row and another generation bump), because b2 never completed and the runtime rejects the later boundary before any adapter runs. The card allows records; nothing is dispatched and the authority does not change. The same happens to any caller that feeds the runtime directly after an omission halt.
- **The repeated silence report is suppressed, not deduplicated.** Under INTERVENTION, `check_source_silence` returns before computing an anchor (`:854–:855`). The deduplication itself is `_halt_db`'s `INSERT OR IGNORE` (`:1871`), exercised here through `halt()`.
- **The bootstrap invalidation names the first detector.** Under the loop that is `feed-silence`, not `barrier-expired` (`book_bootstrap.py:102–:103`).
- **The precondition check calls one private owner method.** To assert "the settlement binding validates" before an attempt, the test calls the owner's existing `_validate_settlement_binding` inside its existing `_transaction`, the same check `_activate_bootstrap` runs first. That check writes only when it refuses; the test asserts `None` and an unchanged incident list. No interface was added.
- **The late-bar node is a regression pin, not a new omission detector.** It needs no omitted slot; a loop cadence slower than `BAR_SLACK` is enough.

## 4. What the bootstrap evidence means (card §1)

`book_bootstrap.py` is the offline one-use bootstrap. The refused re-activation shows how **the current owner implementation** behaves: any incident invalidates the bootstrap (`:1876`), a reboot keeps the first reason, and activation after that is refused. **It is not proof of a complete production re-arming policy.** Incidents are not keyed by session, so the owner also refuses activation in every later session. That is stricter than §A11.2 requires.

## 5. Outstanding obligation

**A later-session re-arming design** is an explicit outstanding obligation for TB-I3 and the resume decision (halt/resume §4). No resume mechanism exists (halt/resume §4.1, *Implementation status*), and this card built none. This evidence also does not establish live feed behavior or arrival timing, a production re-arming policy, or the cause of the H8(b) MGC omission (card §5).

## 6. Verification

Run from the worktree root with `.\fp.ps1` on the ops environment, `C:\Users\joshu\multi_firm_operations\tmp\ops-env\Scripts\python.exe` (Python 3.13.2). The pytest records below bind commit `19bf582` (the test commit) with a clean working tree. This note and the card return section add documentation only.

| Command | Record (`.cache/fp-verification/…/record.json`) | status | verification_exit_code | source_stable | Result |
|---|---|---|---|---|---|
| `.\fp.ps1 doctor` | (none; doctor prints no record) | — | — | — | OK: 62 locked packages matched |
| `pytest tests/ops/test_feed_omission_session_end.py -q` | `20260927T185850Z-5dcd2ca62d82` | completed | 0 | true | 16 passed |
| `pytest tests/ops/test_feed_omission_session_end.py tests/ops/test_attended_incident_rehearsal.py tests/ops/test_four_leg_runtime.py -q` (card §4) | `20260927T185936Z-c4b5bf30ce8d` | failed | 1 | true | 50 passed, 3 skipped, 1 xfailed, **1 failed (pre-existing, below)** |
| the two regression modules with `--deselect` of that node | `20260927T190027Z-5ed618528491` | completed | 0 | true | 34 passed, 3 skipped, 1 xfailed |
| `.\fp.ps1 check` | `20260927T190057Z-835ecc659d3e` | failed | 1 | true | stops at `governance-prose-control-chars` (pre-existing, below) |
| `check` on the corrected tree `768f9b3d` (coordinator, Linux: `python3 -I scripts/fp.py --env <ops-env> check`, CPython 3.11.15, clean tree) | `20260927T192510Z-75cc3db591e2` | completed | 0 | true | all gates pass; supersedes the failed record above |

**Disclosed pre-existing failures (neither caused nor fixed here):**
- **`test_attended_incident_rehearsal.py::test_missed_acknowledgment_never_changes_halt_or_permission` fails on Windows.** `FileAckNotifier.acknowledge` (`c1_rail_telemetry.py:220`) writes a filename containing `:`, which gives `OSError: [Errno 22]`. It passes on Linux CI and is routed separately (card §9). Every other regression node passes, including the correctly-handled-refusal and incomplete-barrier-before-expiry nodes. The skips need the private runtime inputs, and the XFAIL is the recorded CC-3 variance.
- **`.\fp.ps1 check` fails at `governance-prose-control-chars`** on a form-feed (U+000C) at line 171 column 7 of the card, inside the coordinator's §9 dispatch record (commit `e1635d8`): `` `.\fp.ps1 doctor` `` was written as `.` + FF + `p.ps1`. Mid-task, the coordinator recorded a §9 variance authorizing the worker to replace that one byte. The session's permission classifier denied the edit, so the worker did not apply it. *[Resolved 2026-09-27: the coordinator removed the byte in `768f9b3d`, and `check` on that corrected tree exits 0, record `20260927T192510Z-75cc3db591e2` (record.json SHA-256 `8c90ac952a1ae90639b405f5e96e6687c660c772975d0a33068a234711333464`). The failed record above binds the earlier tree only.]* The gate runner stops at the first failure. A diagnostic run of every `check`-tier gate from the same manifest, continuing past failures, found **only** that failure; the other 28 gates exit 0.
