# H5(b) synthetic attended-incident rehearsal: evidence (2026-09-27)

**Status:** EVIDENCE, synthetic. Worker return for [handoff H5 step (b)](https://github.com/Joshua-Asante/first-passage/blob/939cc2a/docs/briefs/handoffs/2026-09-27-h5b-attended-incident-rehearsal.md). The card was dispatched at `24d2268`, amended at `1d83e26` (§10, *Variance 2026-09-27*) and again at `939cc2a` (the operator's late-bar ruling), on PR [#520](https://github.com/Joshua-Asante/first-passage/pull/520). **Acceptance is the coordinator's, and it is partial:** S1's second node is a recorded XFAIL, and CC-3 stays open. The operator merges.

**Evidence class:** *Synthetic / replay engineering* (deployment-checklist addendum §2). Every case runs against the existing owners in a disposable `tmp_path` store. The account, session, clock, identifiers and figures are all synthetic. No rail was armed or deployed. No broker, vendor or account was contacted, and nothing was sent to any external channel. A synthetic result here resolves no obligation that needs a real producer.

**Tests:** `tests/ops/test_attended_incident_rehearsal.py`. It has the 15 acceptance nodes of the amended card: 14 pass and 1 is XFAIL(strict). The rehearsed ruling is [incident ADR §A11.2](https://github.com/Joshua-Asante/first-passage/blob/939cc2a/docs/adr/2026-09-17-bounded-platform-protection-incident-contract.md#a112--operator-ruling-no-same-session-restart-of-automation-after-an-incident-2026-09-27), as applied by [halt/resume §4.1](https://github.com/Joshua-Asante/first-passage/blob/939cc2a/docs/spec/2026-09-14-tb-s3-halt-resume-contract.md#41-amendment-2026-09-27-incident-versus-correctly-handled-refusal).

## 0. Read-first result

- **Anchors:** every §0 anchor matched at the dispatch revision. `ops/` and `tests/` have no diff across `521d8f2`, `24d2268`, `1d83e26`, `939cc2a` and `origin/main` `5ad04cf`.
- **The restart write:** it is at `book_account_owner.py:387-389`, inside the `:383-389` anchor range.
- **The feed-silence halt:** it is at `:865-866`, inside the `:855-866` range; the function starts at `:847`.
- **#519 trace:** its findings are reused, not redone (`8c15f18:docs/notes/2026-09-26-account-fence-four-state-trace.md` rows `:12`, `:64`, `:104`).

## 1. Cases (one row per §2 case)

The synthetic clock starts at `NOW` = 2026-09-15T14:00Z. Each state below is (permission, authority, generation). "Rows" are the rows of the owner's `incidents` table. Every activation check uses a binding that is otherwise fresh, so the refusal `fresh bootstrap entitlement required` is caused by the incident, not by stale evidence.

| # | Node(s) | §2 row / §4.1 class | Before | After | Verdict |
|---|---|---|---|---|---|
| S1 | `test_lost_entry_response_blocks_risk_add_at_once` | `:26` uncertain outcome: **incident** | RUNNING, NORMAL, 1; 0 rows | Entry transport `unknown`. At +1 s another leg's risk-add is refused `unknown_order`, and the broker received 1 command | **PASS**: risk-adds are blocked at once |
| S1 | `test_lost_entry_response_terminal_does_not_restart_automation_in_session` | same | RUNNING, NORMAL, 1; 0 rows | After an accepted, postdating `cancelled` terminal at +2 s: still RUNNING, NORMAL, 1 with 0 rows, and the risk-add at +3 s is `accepted` (a 2nd broker command). Observed with `--runxfail`: `assert ('RUNNING', 'NORMAL') == ('HALTED', 'INTERVENTION')` fails | **XFAIL(strict)**, the §7 (B) variance; see §4 |
| S2(a) | `test_stale_broker_fact_halts_and_blocks_same_session_activation` | `:26` loss of required evidence: **incident** | RUNNING, NORMAL, 1; 0 rows | A fill aged `MAX_FACT_AGE` + 1 s gives HALTED, INTERVENTION, 2, with row `stale-fact:exec-stale` (reason `execution`). Bootstrap `ineligible`, invalidated as `incident:stale-fact:exec-stale`. A later fresh fill is recorded, but the state and rows are unchanged. Risk-add refused `intervention_fence`; activation refused | **PASS** |
| S2(b) | `test_feed_silence_halt_survives_feed_recovery_in_session` | `:28` via `:27`: **incident** at timeout expiry | RUNNING, NORMAL, 1 after a complete barrier at `NOW` | Exactly at the preserved timeout (`2 × 15 min + 30 s`), still RUNNING. At +1 s past it: HALTED, INTERVENTION, 2, with row `feed-silence:<session>:<NOW>` (reason `feed`). After a fresh complete barrier at `NOW + 45 min`, the state and rows are unchanged. Risk-add refused `intervention_fence`; activation refused | **PASS**: feed recovery restores nothing |
| S3 | `test_missed_acknowledgment_never_changes_halt_or_permission` | attendance (§3) | HALTED, INTERVENTION, 2 after an S2(a) incident | Alert written at T0. Not acknowledged at T0 + 60 s. Late acknowledgment at T0 + 180 s. The full `status()` and the incident rows are identical before the alert, after the missed window and after the late ack. Risk-add refused; activation refused | **PASS**: acknowledgment changes nothing (§2 of this note) |
| S4 | `test_restart_during_incident_halt_boots_halted_with_new_generation` | `:33` restart after an incident (settled) | HALTED, INTERVENTION, 2; 1 row | Re-boot on the same store: HALTED, INTERVENTION, 3 with a **new boot ID**. The incident rows are retained. Bootstrap stays `ineligible`, and the first reason (`incident:stale-fact:exec-stale`) is kept | **PASS** |
| S4 | `test_activation_refused_after_incident_and_restart_in_same_session` | same | HALTED, INTERVENTION, 2 | Two successive restarts give generations 3 and then 4. After each, risk-add is refused `intervention_fence` and activation is refused. 0 broker commands | **PASS** |
| S5 | `test_ambiguous_protection_halts_into_intervention_and_fences_mutations` | `:26` protection fault: **incident** | RUNNING, NORMAL, 1, with MYM protected (2 fills) and MNQ open but never protected | Each of 3 ambiguous snapshots (foreign **identity** epoch; **quantity** +1; **ownership** by an unowned fill) gives HALTED, INTERVENTION, 2 with row `protection:invalid-snapshot:ambiguous-<kind>` (reason `protection`). Tighten (MYM stop 98→99), attach (MNQ, unprotected), risk-add, cancel and exit are each refused `intervention_fence`, `not_attempted`. No new broker command | **PASS**: every runtime mutation is fenced |
| S5 | `test_activation_refused_after_protection_incident_in_same_session` | same | as above | Activation refused for all three kinds; state unchanged | **PASS** |
| S6 | `test_operator_halt_leaves_no_same_session_activation_path` | `:26` operator stop: **incident** (O-6, decided 2026-09-27) | RUNNING, NORMAL, 1; 0 rows | `halt(..., "operator")` gives HALTED, INTERVENTION, 2 with 1 row (reason `operator`). A duplicate report is idempotent (still generation 2, 1 row). Risk-add refused; activation refused | **PASS** |
| S7 | `test_capacity_refusal_leaves_session_running` | `:35`: **not an incident** | RUNNING, NORMAL, 1 (settled at peak, NORMAL mode) | Aegis reserves 8 contracts, the full 80-micro cap. An MNQ entry is refused `insufficient_observed_capacity`. After Aegis's postdating terminal, the next MNQ entry is `accepted`. Still RUNNING, NORMAL, 1 with 0 rows | **PASS** |
| S7 | `test_zero_size_sizing_refusal_leaves_session_running` | `:35` | RUNNING, NORMAL, 1 | A 10⁶-point stop is refused `zero_size` with no broker command. The next entry is `accepted` (quantity > 0). Still RUNNING, NORMAL, 1 with 0 rows | **PASS** |
| S7 | `test_duplicate_signal_refusal_leaves_session_running` | `:35` recognized duplicate | RUNNING, NORMAL, 1 | The same signal under a new delivery occurrence is refused `duplicate_operation` (1 broker command in total). The next entry on another leg is `accepted`. Still RUNNING, NORMAL, 1 with 0 rows | **PASS** |
| S7 | `test_incomplete_barrier_before_expiry_leaves_session_running` | `:30` before expiry: **not an incident** | RUNNING, NORMAL, 1 (four-leg runtime, `FourLegRuntime`; fixtures reused from `test_four_leg_runtime.py`) | Three of four legs deliver bar `NOW`; the MNQ adapter holds an entry stamped with that bar. Before expiry: `on_completed_bar` returns nothing, no adapter has evaluated the bar, no action batch is prepared, there are 0 broker commands, 3 partials are retained and there is no barrier. Still RUNNING, NORMAL, 1 with 0 rows. The fourth leg then arrives at `NOW + 10 s`, before the `bar_period + 30 s` expiry, and completes the bar. That bar's entry is the next valid request and is `accepted` (1 broker command); the barrier is recorded complete. Still RUNNING, NORMAL, 1 with 0 rows | **PASS** |
| — | `test_only_bootstrap_activation_writes_running_permission` | structural | — | See §3 | **PASS** |

**Stale individual signal (the S7 sub-case removed by the card's §10 variance at `1d83e26`):**
- **Not rehearsed.** No node, xfail or stand-in exists for it.
- **Finding, ruled not a defect:**
  - No owner implements a `:35` stale-individual-signal refusal: `BookAccountOwner.dispatch` never compares a signal's `bar_time` with `now`.
  - The nearest behavior halts. A late completed bar makes the runtime halt the whole book into INTERVENTION (`ops/c1_signal_daemon/book_runtime.py:350-353`). The existing test `tests/ops/test_four_leg_runtime.py::test_stale_or_future_completed_bar_halts_before_dispatch` pins that behavior.
  - Separately, a wrong-bar intent is recorded as an input incident and halts (`book_runtime.py:208-217`).
- **Operator ruling, 2026-09-27:** "a late bar is a source incident; the halt is correct". It is recorded in [halt/resume §4.1, *Qualifications*](https://github.com/Joshua-Asante/first-passage/blob/939cc2a/docs/spec/2026-09-14-tb-s3-halt-resume-contract.md#41-amendment-2026-09-27-incident-versus-correctly-handled-refusal) and in the card's §10 at `939cc2a`. So the late-bar halt is correct behavior, not a defect.
- **The ruling covers late bars only.** It does not classify a future bar, a bar outside the bound session, or a wrong-bar intent, and this note makes no claim about them.

**Observation: barrier completeness is gated by the runtime, not by owner `dispatch` (not a defect claim).**
- **Revision history.** The first revision of the S7 incomplete-barrier node (`fbfd925`) dispatched directly on the owner an intent stamped with the incomplete bar's time, and the owner admitted it. That test was evidence against `:30`, so it was replaced by the runtime-level node above after the coordinator's review.
- **The owner does not check.** `BookAccountOwner.dispatch` (`book_account_owner.py:1455-1461`, `_dispatch_locked` `:1463` onward) does not check barrier completeness for an intent's `bar_time`. The check lives in `FourLegRuntime._on_completed_bar` (`ops/c1_signal_daemon/book_runtime.py`). It returns before any adapter runs until all four legs of a bar are present (`if len(slot) != len(LEG_ORDER): return None`). Only then does it record the barrier and dispatch that bar's actions (`:390-412`).
- **No production path reaches owner `dispatch` for a new bar's actions without that barrier.** The only caller of the public `dispatch` is `c1_rail_listener.handle_book_action` (`c1_rail_listener.py:80-91`). Its docstring says: "This is the offline Phase-2 boundary. The owner has no production route; its only sender is the explicit `SyntheticBroker` Python test seam". Its only callers in `ops/` are `book_runtime.py:412`, `:418` and `:456`. `:456` is `redeliver_prepared_boundary`, which re-drives a batch already prepared from a completed barrier. `c1_rail_http_server.py` constructs no `BookAccountOwner`; it boots only `BookHaltStore`, at `:431`. A repository-wide search outside `tests/` finds `handle_book_action`/`BookAccountOwner` only in `book_account_owner.py`, `book_migration.py`, `c1_rail_listener.py` and `book_runtime.py`. The owner's internal re-entries into `_dispatch_locked` replay durable occurrences that were already prepared; none originates a new bar's risk-add:
  - `resume_closes`, close-pending demands (`:1265`);
  - `advance_schedule`, scheduled cancel/flat (`:1785`);
  - `resume_takeover`, takeover intents (`:1862`);
  - the takeover owner (`book_takeover_owner.py:537`).
- **Conclusion.** Under today's code the `:30` gate is the runtime's by design. No TB-I3 item is raised by this observation.

**OPEN items not rehearsed as decided:** O-1 (stale order-level evidence; H4's), O-2, O-3, O-4 (restart with no prior incident) and O-5 are asserted neither way. S4 covers only a restart **after** an incident.

## 2. Notification and 60 s escalation (card §3)

| Item | Result | Basis |
|---|---|---|
| Incident → notification | **ABSENT**; owed to Phase 5 WP2 / T13 | `book_account_owner.py`, `book_halt.py`, `book_protection_owner.py` and `book_bootstrap.py` contain no `notif`, `alert` or `escalat`. `OperatorNotifier`/`FileAckNotifier` are called only on the legacy single-leg path: `c1_rail_listener.py:333`, `:383` and `:421` (CRITICAL on transport_unknown and telemetry failures), and `c1_rail_http_server.py:506` and `:557`. No book owner emits anything when it halts. In S3 the harness writes the alert itself. |
| Alert write → acknowledgment (`FileAckNotifier`) | **MEASURED, local consumer only** | This is the Phase 5 WP2 phrase "mocks prove only the local consumer behavior". On a synthetic clock (the module's `utc_now_iso` is patched in the test): alert `ts_utc` = T0; `is_acknowledged` false at T0 + 60 s; the ack file's `acked_utc` = T0 + 180 s; `is_acknowledged` true after it. The owner's full `status()` and its incident rows compare equal through all three. The notifier holds no owner reference and has no path to permission or to a broker command. A local file acknowledgment is **not delivery**. |
| 60 s alternate-channel escalation | **ABSENT**; owed to Phase 5 WP2 / T13 | No owner implements it. In `ops/**/*.py`, `escalat` occurs once, at `c1_rail_slippage.py:20` (unrelated). No harness stand-in is counted. |
| Immediate delivery-failure routing | **ABSENT**; owed to Phase 5 WP2 / T13 | No owner has more than one channel. |
| Independent missed-heartbeat monitor | **ABSENT**; unselected (halt/resume §3) | `ops/c1_signal_daemon/heartbeat.py` is the daemon's `GET /` liveness snapshot, not an external monitor. |
| Real delivery and acknowledgment timing on the operator's channel | **OWED** to T13 / Phase 5 WP2 (card §10) | No operator-run leg was requested, and no agent sent anything. |

## 3. Structural scan

`test_only_bootstrap_activation_writes_running_permission` parses every `ops/c1_rail/*.py` with `ast`. It collects each string literal, joining implicitly concatenated literals and reducing f-strings to templates, and asserts four things:

1. **No bound-parameter writes:** no `permission=?` or `authority=?` anywhere, so no parameterized value is left unresolved.
2. **No formatted table names:** no `INSERT`/`UPDATE` has a formatted-in table name.
3. **The `owner_state` write sites are exactly these seven:**
   - `book_account_owner.py`: `_boot_locked` twice (`:334` creation and `:388` restart, both HALTED/INTERVENTION), `_next_sequence` (`:680`, sequence only), `_advance_schedule_locked` (`:1748`, HALTED/SCHEDULED_EXIT) and `_halt_db` (`:1873`, HALTED/INTERVENTION);
   - `book_bootstrap.py:_activate_bootstrap` (`:174`);
   - `book_migration.py:migrate_book_owner` (`:412`, HALTED/INTERVENTION).

   The positional `INSERT` carries literal permission and authority values.
4. **Only one RUNNING/NORMAL site:** the only statement anywhere that sets `'RUNNING'` or `'NORMAL'` is `book_bootstrap.py:_activate_bootstrap`, `UPDATE owner_state SET permission='RUNNING', authority='NORMAL'`.

**Result: PASS.** It matches the card's greps at `521d8f2`.

**Mutation check.** This was a scratch copy of `ops/c1_rail/` outside the tree; nothing was committed. Planting any of the following makes the test fail, and the unmutated tree passes:
- a second literal RUNNING/NORMAL write;
- a bound `permission=?` write;
- an f-string `UPDATE {table}` write.

The scan covers permission transitions only. An admission-level restart, where permission stays RUNNING and nothing is written, is S1's and S7's (see §4).

## 4. Restart and restore traces

- **Restart (S4).** Each boot on an existing store:
  - invalidates the bootstrap (`book_account_owner.py:387`), keeping the first invalidation reason;
  - writes a new boot ID with generation + 1, HALTED/INTERVENTION (`:388-389`);
  - retains every incident row.

  After two restarts, generation is 4, and activation is still refused because the bootstrap is ineligible and bound to an older boot (`book_bootstrap.py:127-131`).
- **Restore from backup** is not exercised by this card; that is Phase 5 WP3. The nearest existing evidence is the migration path, which forces HALTED/INTERVENTION with a `migrated`, `ineligible` bootstrap (`book_migration.py:412`, `book_bootstrap.py:53-54`). The reused `test_book_bootstrap_migration.py::test_empty_history_cannot_rearm` covers it.
- **Reused, not duplicated:**
  - `test_book_halt.py::test_running_injected_into_database_never_grants_permission`;
  - `test_book_bootstrap_migration.py::test_empty_history_cannot_rearm`, `::test_running_activation_is_noop_after_activity` and `::test_halt_wins_serialized_race_with_fresh_activation`;
  - `test_c1_rail_telemetry.py::test_file_ack_notifier_notify_and_acknowledge`;
  - H4's pending `test_refreshed_evidence_never_restores_permission_after_incident_halt` and `test_stale_evidence_blocks_admission_loosening_and_takeover`, on H4's unmerged branch and cited by name only.

## 5. S1 variance and defects

**S1 XFAIL (card §7 option (B), a recorded coordinator variance from the parent H5 stop condition "Stop and return; it is a defect").**
- **Pinning:** `test_lost_entry_response_terminal_does_not_restart_automation_in_session` is pinned `xfail(strict=True)`, with a reason naming CC-3 and §A11.2.
- **What the XFAIL is not:** acceptance of §A11.2 behavior. H5 step (b)'s acceptance is therefore **partial**, and CC-3 stays an open defect.
- **What `strict` means:** if a repair makes the node pass, the XPASS fails the suite, so the pin cannot silently outlive the fix.

| Defect | Evidence | Owner |
|---|---|---|
| **CC-3.** No halt for an ordinary unknown entry outcome (§2 `:26`), and risk-add admission resumes in the same session once an accepted, postdating terminal clears the fence (`book_account_owner.py:795`, `:1608-1609`). Under §A11.2 no same-session resumption is permitted at all. | S1 nodes: blocked at once (PASS); re-admitted with permission RUNNING and 0 incident rows (XFAIL). Consistent with the #519 trace `:12` and `:64`. | TB-I3 / T09 (open; not repaired here) |
| None other found. | The late-bar halt was ruled correct (§1). | — |

## 6. Synthetic versus owed (card §4, filled in)

| Established by this card (synthetic) | Owed elsewhere |
|---|---|
| **Owner-level incident-versus-refusal behavior.** S2(a), S2(b), S4, S5 and S6 end automation for the session with no activation path. S7 capacity, zero size and duplicate (owner level) refuse the request only, and an incomplete barrier before expiry (runtime level) dispatches nothing from that bar without a halt. S1 blocks at once but **re-admits** (CC-3, XFAIL). | Real delivery and acknowledgment timing on the operator's qualified channels; 60 s alternate-channel escalation; immediate failure routing; the external heartbeat monitor (all Phase 5 WP2, T13) |
| Restart during an incident halt (new boot ID and generation; rows retained; bootstrap ineligible) | H2 commissioning traces (`COMMISSIONING_OBSERVATION`), folded in before any session that could produce an unresolved request |
| Structural absence of any RUNNING/NORMAL transition other than bootstrap (plus the mutation check) | The ordinary-unknown halt (CC-3, TB-I3/T09); the durable resume/activation owner (TB-I3, Phase 5 WP4) |
| Local `FileAckNotifier` behavior on a synthetic clock (MEASURED, local only) | Incident → notification emission (ABSENT; Phase 5 WP2 / T13) |
| Evidence class *Synthetic / replay engineering* | Restore from backup (Phase 5 WP3); O-1 to O-5 (their §4.1 owners) |

## 7. Verification records

Run through this checkout's launcher, `python3 -I scripts/fp.py --env <ops-env outside the tree>`, with interpreter Python 3.11.15. Every run below had a clean tree. The first five ran on `fbfd925`. The last two ran on `ae9fe50`, which rewrote the S7 incomplete-barrier node through the four-leg runtime after the coordinator's review. Only this section changes after `ae9fe50`. Each `record.json` is under this checkout's `.cache/fp-verification/<id>/`, which is gitignored and local to the worker's checkout.

| Command | Record ID | Result |
|---|---|---|
| `doctor` | (no record) | Environment valid; 62 locked packages matched. "Optional signing dependency: absent" (`cryptography`). |
| `python -m pytest tests/ops/test_attended_incident_rehearsal.py -q` | `20260927T100900Z-6519da6c5820` | completed, exit 0, `source_stable` true: 14 passed, 1 xfailed |
| `python -m pytest` on the six related suites (`test_book_halt.py`, `test_book_bootstrap_migration.py`, `test_book_account_owner.py`, `test_book_protection_evidence.py`, `test_c1_rail_telemetry.py`, `test_pr409_review4.py`), all unchanged | `20260927T100907Z-460256eb6f92` | completed, exit 0, `source_stable` true: 187 passed |
| `test-ops` | `20260927T100925Z-cfd9197073ef` | **failed**, exit 1, `source_stable` true: 2585 passed, 36 skipped, 1 xfailed, **1 failed** |
| `check` | `20260927T101047Z-4f0a7edcbc75` | completed, exit 0, `source_stable` true |
| `python -m pytest tests/ops/test_attended_incident_rehearsal.py -q`, at `ae9fe50` | `20260927T101716Z-9217fb7864f2` | completed, exit 0, `source_stable` true: 14 passed, 1 xfailed |
| `check`, at `ae9fe50` | `20260927T101719Z-7885a9562283` | completed, exit 0, `source_stable` true |

**The `test-ops` failure comes from the environment, not from this change.** The failing test is `tests/ops/test_qualification_isolation.py::test_qualification_suite_in_clean_process`. Its clean child process cannot import `tests/ops/qualification/test_result_key_binding.py`, `test_review_repairs.py`, `test_seal.py` or `test_trust_domain.py`, because of `ModuleNotFoundError: No module named 'cryptography'`. That is the optional signing dependency `doctor` reports absent from this operations environment. None of those files is touched here. **The complete `test-ops` suite is therefore not claimed to pass.** The coordinator reproduced this failure on unmodified `origin/main` in the same environment.
