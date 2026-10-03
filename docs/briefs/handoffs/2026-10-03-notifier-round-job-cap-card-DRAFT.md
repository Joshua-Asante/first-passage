# Notifier per-pass job cap (TB-I3-HOST P7) — build card

**Date:** 2026-10-03.
**Status:** **DRAFT.** Written under coordinator (3)'s #628 build authority, which dispatched this docs-only follow-up card on 2026-10-03. Coordinator (3) freezes it (§12). Nothing here is dispatched.
**Base:** origin/main `6e679cc` (#628 merged). `git diff 6e57fda 6e679cc` is empty for `ops/c1_rail/book_incident_notifier.py` and `tests/ops/test_book_incident_notifier.py`, so #628 anchors cited at `6e57fda` hold here. Other revisions read: #651 at `origin/claude/tb-i3-host-card` `fa13c57` (DRAFT); #635 at `origin/claude/dmon-grafana-binding-card` `736e186` (DRAFT). Branch anchors hold only at those heads.
**Brief type:** CC handoff, code build (TDD) behind a named file boundary.
**Parent:** the #628 build card (`docs/briefs/handoffs/2026-10-02-book-incident-notifier-build-card.md`). #651 records this work as P7, "a per-round job cap on `publish_due`, from the #628 owner, in #628 or a follow-up (OQ-HOST-2)" (`fa13c57:99`, `:249`), and P7 blocks #651's freeze.
**Finding being closed:** `publish_due` runs one job round for every due pending job, with no limit (`6e679cc:447-461`). Pending jobs persist until delivered, so a notifier loop's duration grows with the backlog, and no host input bounds it (#651 §0.5 item 6, `fa13c57:79`).
**Selected outcome:** A validated `NotifierConfig.max_jobs_per_round` (positive int, default 10), exposed through `from_mapping` and `resolved()`. Each `publish_due` pass runs at most that many due jobs: first attempts first, then the oldest due, then creation order. Jobs over the cap stay pending, unchanged, and keep their due time.
**Ownership:** One Opus/CC worker builds it (§11). Coordinator (3) accepts it. Joshua merges.
**Return boundary:** A pushed `claude/*` branch that touches only the §5 allowed files, or a precise blocker.

```yaml authority
seat: worker
parent: docs/briefs/handoffs/2026-10-02-book-incident-notifier-build-card.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push]
constraints:
  - no_main_write
  - no_merge
  - no_pr_unless_coordinator_records_it
  - allowed_files_section_5_only
  - no_owner_record_edit
  - no_rail_deploy
  - no_rail_arm
  - no_account_traffic
  - no_broker_vendor_firm_or_provider_contact
  - no_external_send
  - no_provider_account_or_spend
  - no_credentials_or_private_data_in_repo
  - no_concrete_channel_binding
  - no_operator_decision_taken
  - no_host_wiring
  - no_existing_test_edit
  - channel_kinds_untouched
acceptance:
  - "Every red-first test in §6 (RC1-RC6) fails at the base revision and passes at the returned head; the failing-first run is recorded"
  - "tests/ops/test_book_incident_notifier.py passes unchanged (59 tests at 6e679cc)"
  - "git diff --stat origin/main...HEAD lists only §5 allowed files, and the notifier diff stays inside §5's line ranges"
  - "python -I scripts/fp.py test-ops and python -I scripts/fp.py check: status completed, exit 0, source stable; or a pre-existing failure disclosed with its reproduction on unmodified origin/main"
  - "python -I scripts/fp.py test (full suite): recorded before coordinator (3) acceptance"
```

## §0 — Read first (report before writing code; otherwise `NEEDS_CONTEXT`)

| Input | Where | Read |
|---|---|---|
| Notifier (merged #628) | `ops/c1_rail/book_incident_notifier.py` at `6e679cc` | `MAX_OUTSTANDING_PUBLISHES` `:63-66`; `CHANNEL_KINDS` `:67-70`; `_CONFIG_KEYS` `:74`; `NotifierConfig` `:205-256` (fields `:208-212`, `__post_init__` `:214-234`, `from_mapping` `:236-249`, `resolved` `:251-256`); `_journal` `timeout=5` `:304`; `poll` `:396-421` (job created with `next_attempt_at` = poll time, `:413-415`); `run_once` `:425-436`; `liveness` `:438-445`; `publish_due` `:447-461`; `_publish_round` `:463-499` (admission `:470`, close `:486`); `_pending` `:501-506`; `_transition` `:508-534` (rounds and backoff `:522-530`); `_refusal` `:536-552`; `_bounded_publish` `:554-580` (`join` `:575`) |
| Notifier tests (59 at `6e679cc`) | `tests/ops/test_book_incident_notifier.py` | `Clock` `:59`; `_config` `:70-77`; `_notifier` `:80-89`; `hanging` fixture `:1198-1210`; `_due_rounds` `:1213-1217`; T21 `:1255-1276`; T22 `:1279-1294` (10 due jobs in one pass) |
| #628 build card | `docs/briefs/handoffs/2026-10-02-book-incident-notifier-build-card.md` | Form; authority block `:13-39`; OQ-2 "no retry cap" `:68`; §0.6 rebuild limits `:86-90`; §0.7 `:92-109`; §0.8 J0-J5 `:111-146`; §5 `:223-242`; §8 `:301-310`; §11 `:345-347` |
| TB-I3-HOST card (#651) | `git show fa13c57:docs/briefs/handoffs/2026-10-03-tb-i3-host-heartbeat-wiring-card-DRAFT.md` | §0.5 items 5-6 `:78-79`; P7 `:99`; §2 `max_step_interval` `:109`, `max_round_duration` `:113`, threshold (b) `:116-121`; §3.1 `max_jobs_per_round` `:129-135`; HH4 `:195`; HH7 `:198`; OQ-HOST-2 `:249`; OQ-HOST-4 `:251` |
| D-MON IRM binding card (#635) | `git show 736e186:docs/briefs/handoffs/2026-10-03-dmon-grafana-irm-binding-card-DRAFT.md` | `CHANNEL_KINDS` entry `:116`; `alert_uid` = idempotency key `:118`; retry interaction ("no cap") `:133`; CLI read-only pre-check `:140`; §5 allowed notifier edit `:159`; existing tests unedited `:170` |
| Owner read seam | `ops/c1_rail/book_account_owner.py` | `read_incidents` `:804-812` (`timeout=5` `:811-812`) |
| Measured closures | `docs/notes/2026-09-29-s5-c3-record/stage1c-equivalence/stage1c_closure_table.py.txt`; `docs/briefs/handoffs/2026-10-02-h9-cprime-runtime-identity-build-DRAFT.md` `:117`, `:145`; `docs/notes/2026-09-27-s5-part-a-measurement/`; `docs/briefs/handoffs/2026-09-24-tradeify-t00-p7-closure.md:630` | §2 |
| Rules | `AGENTS.md` *Python environment* `:220-227`, *Configuration as code* `:229-238`; `scripts/seat_authority.yml:105-108` | |

**The report states:** the dispatch revision; whether #635's D-MON-1 build has landed and which lines of `book_incident_notifier.py` it changed; whether #651 has frozen and the cap name it records; and every anchor that moved.

## §0.5 — Clarifications and recorded decisions

1. **Terms.** A *pass* is one `publish_due` call. A *job round* is one `_publish_round` (one job across the channels), as #628's code uses "round". The field keeps #651's name, `max_jobs_per_round`: #651's notifier round is one `run_once`, which holds exactly one pass.
2. **Order: first attempts first, then the oldest due, then creation order.** The sort key is `(rounds > 0, next_attempt_at, rowid)`. It differs from the dispatch's example (oldest `next_attempt_at`, `incident_key` tiebreak) on drafting evidence. The probe replaced `publish_due` in memory and ran the unchanged #628 suite at `6e679cc`; no file changed.
   - **`incident_key` tiebreak:** 8 of 59 #628 tests fail, including T21, T22, J1, J2 and J5. They pin creation order among jobs that share a due time. The `rowid` tiebreak passes 59.
   - **Oldest due alone:** a new incident waits behind every due retry. Simulation (cap 1, two failing jobs): a third incident committed at pass 3 was not attempted in passes 3 or 4. The chosen key attempts it at pass 3.
   - **Fewest rounds first:** also attempts new incidents first. But a job with many failed rounds then waits until every newer due job has as many rounds (derived, not run).
   - **`rowid` order with a cap:** it starves jobs. Simulation (5 jobs, cap 2, all failing, all due every pass): jobs 1 and 2 ran in every pass, and jobs 3-5 never ran.
3. **Default 10.** This is the smallest value that keeps the #628 suite unchanged. T22 publishes 10 due jobs in one pass, and its `_config` omits the field. Probe: cap 10 passes 59 (both `rowid` and the chosen order); cap 9 fails T22. It is a compatibility default. The host's value is TB-I3-HOST's binding value (`fa13c57:131`), frozen under OQ-HOST-4.
4. **Deferral writes nothing.** A deferral gets no new event kind and no job update; the journal schema is unchanged. A backlog shows in `jobs()`.
5. **OQ-2 is unchanged.** It is a "no retry cap" rule (#628 card `:68`): it limits nothing per job. This cap limits jobs per pass.
6. **Digest.** `resolved()` gains the field, so every configuration's digest changes. `config_digest` is recorded per job and never compared, and no journal is deployed (#628 card `:90`).
7. **Forbidden files** are §5's.

A contradicted default, a missing producer or a necessary edit outside §5 returns NEEDS_CONTEXT.

## §1 — Goal, scope, prerequisites

**Goal.** TB-I3-HOST can declare `max_round_duration` at a stated cap and refuse a notifier whose cap differs (`fa13c57:113`, `:131`, HH4 `:195`, HH7 `:198`). The #628 contract otherwise stays as merged.

**Scope.** One config field with its validation and `from_mapping`/`resolved()` exposure, the `publish_due` selection, and one new test file.

| ID | Item | State at draft | Blocks |
|---|---|---|---|
| P1 | #628 merged | **Done** (`6e679cc`) | Nothing |
| P2 | Coordinator (3) rules OQ-CAP-1 (default) and OQ-CAP-2 (order) | OPEN | Freeze |
| P3 | Sequencing with #635's D-MON-1 worker (§5) | OPEN; recorded at dispatch | Dispatch |

## §2 — Measured-closure check

`book_incident_notifier.py` is in no measured closure. Checked at `6e679cc`:
- **S5 Stage 1c, the C′ card's 68 modules** (`2026-10-02-h9-cprime-runtime-identity-build-DRAFT.md:117`). The closure table script, run as `stage1c_closure_table.py.txt . 6e679cc 6e679cc`, lists 68 measured and 63 staging modules. None is the notifier. Its `ops/c1_rail` members outside `qualification/` are `__init__`, `book_policy`, `book_schedule`, `ed25519_verify` and `policy_fingerprint`.
- **S5 records.** `rg book_incident_notifier docs/notes/2026-09-27-s5-part-a-measurement docs/notes/2026-09-29-s5-c3-record` has no match.
- **T00 P7 first-party closure** (40 modules, `2026-09-24-tradeify-t00-p7-closure.md:630`). The list is not in the repository; the C′ card attaches it at D8 (`:145`). Static evidence instead: outside `docs/`, `git grep book_incident_notifier 6e679cc` matches only the module's own test and the path string in `scripts/check_durable_store_pragmas.py:54`. No module imports the notifier, so no closure rooted elsewhere reaches it.

The worker re-runs the table from `origin/main` to `HEAD` (§7).

## §3 — Design

1. **Field.** Add `max_jobs_per_round: int = 10` to `NotifierConfig` after `retry_max_s` (`:211`).
   - **Validation.** `__post_init__` refuses a `bool`, any non-`int` and any value below 1, raising `NotifierConfigError("max_jobs_per_round must be a positive integer")`. It runs before the digest. A float such as `2.0` is refused.
   - **Exposure.** `_CONFIG_KEYS` (`:74`) gains the key, so `from_mapping` passes it through (`:248`), and `resolved()` emits it. `config.max_jobs_per_round` and `resolved()["max_jobs_per_round"]` are what TB-I3-HOST compares.
2. **Selection** (`publish_due`, inside `_round_lock`, J0).
   - The snapshot also reads `rounds`. "Due" is unchanged: pending, with `next_attempt_at <= now`.
   - Sort the due jobs by `(rounds > 0, next_attempt_at, rowid)` and run `_publish_round` for the first `max_jobs_per_round`. The existing `ORDER BY rowid` gives the `rowid` rank.
   - Compare `next_attempt_at` as parsed aware datetimes. ISO strings with different UTC offsets do not sort as instants.
   - `now` stays one value per pass. Update the docstring.
3. **Deferral.** A due job beyond the cap gets no write in that pass: no event and no job update. Its `next_attempt_at` stays at or before `now`, so the next pass sees it as due.
4. **Unchanged:**
   - J0-J5 and every writer: `_publish_round`, `_pending`, `_transition`, `_refusal`, `_bounded_publish`, `_record_late`, `record_delivery`.
   - Backoff (`:522-530`).
   - The payload and its idempotency key. #635 sends that key as `alert_uid` (`736e186:118`).
   - `MAX_OUTSTANDING_PUBLISHES` and its reservation.
   - `poll` (J1), `run_once` and `liveness()`. A pass that defers jobs completes normally, so `liveness()` refreshes as before.
   - A job nominated and then closed before admission still uses its slot (J2 returns at once). That can only shorten a pass.
5. **Fairness.** Four facts from the code:
   - **F1.** An attempted job that stays pending gets `next_attempt_at = now_P + delay`, with `delay >= retry_initial_s > 0` (`:522-530`).
   - **F2.** A deferred job is not written (item 3).
   - **F3.** `poll` creates a job with `next_attempt_at` equal to its clock time and a larger `rowid` (`:413-415`).
   - **F4.** The notifier clock does not step backward; #651 already requires it to advance (`fa13c57:78`).

   Guarantees, with X a due job, k the cap, and A the due jobs ahead of X:
   - **A never-attempted X** runs within ⌊A/k⌋ more passes. Each pass runs k jobs ahead of it. A job that runs leaves the never-attempted class. By F3 and F4, a new job sorts behind X.
   - **An attempted X** runs within ⌊(A + N)/k⌋ more passes, where N is the number of incidents committed meanwhile. A job that ran in a pass that skipped X sorts behind X afterwards: by F1 its `next_attempt_at` exceeds `now_P`, which is at least X's. By F2, nothing behind X moves ahead. A new incident is ahead of X only until its first attempt, so it costs X at most one slot.
   - **No job starves.** Incidents are committed owner rows, one per `incident_id` (`INSERT OR IGNORE`), so N is finite. Under persistent failure with no new incident, passes rotate round-robin. Simulation (5 jobs, cap 2): {1,2}, {3,4}, {5,1}, {2,3}, {4,5}, {1,2}.
   - **A pass that raises** (`NotifierStoreError`) ends early with no deferral state. The next pass selects in the same order. `liveness()` does not refresh (`:425-436`).
   - **Residual.** After a journal rebuild, every re-owed incident has never been attempted (#628 card `:86-90`). A new incident then waits behind them, up to ⌊A/k⌋ passes.
6. **Duration bound (TB-I3-HOST's input).** Per pass at cap k with c channels:
   - at most k·c bounded publishes, each at most `publish_timeout_s` τ (`join` `:575`);
   - at most 1 + 2·k·c journal transactions: the snapshot (`:455`), then per (job, channel) one admission (`:470`) and one close (`:486`).

   `run_once` adds one journal transaction (poll, `:411`) and one owner read (`read_incidents`, `timeout=5`). So:

   `max_round_duration <= k·c·τ + (2 + 2·k·c)·W_j + W_o + ε`

   - **W_j** is the declared lock wait per journal transaction. It is 5 s at `BEGIN IMMEDIATE` (`timeout=5`, `:304`). In the default rollback journal, `COMMIT` can wait another 5 s behind a SHARED reader such as #635's read-only pre-check (`736e186:140`), so W_j can reach 10 s.
   - **W_o** is 5 s.
   - **ε** is CPU and fsync time, which no declared bound covers; HH7 measures it.

   Simulation (k = 2, c = 2, τ = 0.05 s, both channels holding past τ): 4 publishes and 9 transactions on the pass thread; `publish_due` took 0.309 s.
7. **Consequence for TB-I3-HOST (routed, OQ-CAP-3).** Take #628's τ = 10 s, c = 2 and k = 1. The bound is 20 + 30 + 5 = 55 s, or 85 s with W_j = 10 s. On the notifier side, #651's (b) needs `2·max_round_duration + P_n + ping_timeout + slack < T_n`, since `max_notifier_loop_interval >= max_round_duration + slack` (`fa13c57:109`, `:113`, `:116-121`). The lean T_n = 60 s therefore needs `max_round_duration` below 30 s. The cap is necessary but not sufficient: TB-I3-HOST must also choose τ, the declared W_j, or T_n.

## §4 — Hypothesis and falsifier

**H:** With `max_jobs_per_round = k`, each pass runs at most k due jobs in the §3.2 order. Each pass is then bounded by k·c·τ plus the declared lock waits. Every pending job still runs within the §3.5 bound, and nothing else in #628 changes.

**Falsifier.** Any one of these refutes H:
- a pass that runs more than k jobs;
- under persistent failure, a due job that does not run within the §3.5 bound;
- a deferred job whose row or events change in the pass that deferred it;
- any #628 test failing, or a change to J0-J5, backoff, the payload or its key, delivery, `record_delivery` or `liveness()`;
- a configuration that accepts 0, a negative value, a non-`int` or a `bool`;
- `resolved()` and `from_mapping` that do not round-trip the cap.

## §5 — Files

**Allowed:**
- `ops/c1_rail/book_incident_notifier.py`, **only** these parts:
  - `_CONFIG_KEYS` (`:74`);
  - the `NotifierConfig` field, its validation and its `resolved()` entry (`:205-256`);
  - `publish_due` and its docstring (`:447-461`).
- `tests/ops/test_book_incident_notifier_round_cap.py` (new).
- This card, for the freeze commit and the executor return only.

**Forbidden (stop and return if a change seems needed):**
- Every other line of `book_incident_notifier.py`, including:
  - `MAX_OUTSTANDING_PUBLISHES` (`:63-66`);
  - `CHANNEL_KINDS` and its comment (`:67-70`), which #635's D-MON-1 worker owns (`736e186:159`);
  - the J0-J5 writers, `poll`, `run_once`, `liveness`, the journal schema and the module docstring.
- `tests/ops/test_book_incident_notifier.py` and every other existing test.
- These files:
  - `scripts/check_durable_store_pragmas.py`, `book_account_owner.py` and every other `ops/c1_rail/book_*.py`;
  - `ops/c1_signal_daemon/**`, including TB-I3-HOST's `book_host.py` and #637's `book_heartbeat.py`.
- Everything the #628 card forbids (`:234-242`):
  - the T00 P7 and S5 measured closures;
  - risk controls and locked surfaces;
  - arming and config;
  - the legacy notifier path;
  - docs and governance.
- The #628, #635 and #651 cards.

**Sequencing with #635's D-MON-1 worker.** Both builds edit `book_incident_notifier.py`, but the hunks are disjoint:
- #635 edits only `:67-70`. This card's nearest hunk is `:74`, and `:71-73` lie unchanged between them, so a three-way merge applies both.
- **Preferred: this card lands first.** Coordinator (3) then re-anchors #635 at its freeze: #635 cites `:205-256` and `:447-461` and says "no cap" (`736e186:133`).
- **If D-MON-1 lands first,** this worker merges current main, re-reads the anchors and keeps the same hunks.
- Neither worker edits the other's lines.

## §6 — Red-first tests and return taxonomy

The tests go in `tests/ops/test_book_incident_notifier_round_cap.py`. They use synthetic incident rows through an injected `read_incidents`, or a real `BookAccountOwner` as #628 does, with a fake notifier clock. The file defines its own helpers and does not import the #628 test module. Run the file at base first and record the failure: the field is absent, so `from_mapping` refuses the key and the constructor refuses the keyword.

| ID | Test | Basis |
|---|---|---|
| RC1 | `test_cap_runs_exactly_k_due_jobs_per_pass_in_order`, with three cases. (a) Five never-attempted due jobs, cap 2, a delivering channel: passes publish jobs [1,2], [3,4], [5] (creation order on ties). (b) Cap 1, two attempted due jobs where the later `rowid` has the earlier `next_attempt_at`: that job runs first. (c) A never-attempted job runs before an attempted job with an earlier `next_attempt_at` | §3.2 |
| RC2 | `test_jobs_over_the_cap_stay_pending_unchanged_and_unlogged`. After a capped pass, each deferred job's row is equal to its row before the pass: `state`, `next_attempt_at`, `rounds`, `channels_lost`, `config_digest`. No event carries its key from that pass. `liveness()` equals the pass's clock time. Every job is delivered in later passes | §3.3, §3.4 |
| RC3 | `test_persistent_failures_rotate_every_job_without_starvation`: five jobs, cap 2, a channel that always rejects, and the clock advanced 60 s (more than `retry_max_s`) before each pass, so every pending job is due every pass. Sets run per pass: {1,2}, {3,4}, {5,1}, {2,3}, {4,5}, {1,2}. Every job runs in any 3 consecutive passes, and run counts differ by at most 1. Also `test_a_new_incident_is_attempted_before_due_retries`: cap 1, two failing due jobs and a third incident committed. The next pass attempts the new incident, and the retry it displaced runs in the pass after | §3.5 |
| RC4 | `test_pass_duration_is_bounded_by_cap_channels_timeout_and_lock_waits`: cap 2, two channels holding every publish past τ = 0.05 s (`FakeChannel.HANG`, released at teardown), five due jobs, fake notifier clock. On the pass thread, `_bounded_publish` is called exactly k·c = 4 times and `_journal` is entered exactly 1 + 2·k·c = 9 times. `run_once` adds exactly one transaction and one `read_incidents` call. Real elapsed time of `publish_due` is at most k·c·τ + (1 + 2·k·c)·5 s. Teardown releases every held publish and joins its thread | §3.6 |
| RC5 | `test_max_jobs_per_round_refuses_invalid_values[0, -1, True, False, 1.0, 2.5, "2", None]`: each value raises `NotifierConfigError`, both through `NotifierConfig(...)` and through `from_mapping` | §3.1 |
| RC6 | `test_max_jobs_per_round_round_trips_through_resolved_and_from_mapping`. The default 10 appears in `resolved()`. For the default and for 3, `NotifierConfig.from_mapping(c.resolved()) == c` with equal digests. Caps 3 and 4 give different digests. A notifier's `config.max_jobs_per_round` equals `resolved()["max_jobs_per_round"]` | §3.1; `fa13c57:131` |
| — | Regression: `tests/ops/test_book_incident_notifier.py` passes unchanged (59) | §0.5 item 3 |

**Mutant evidence for the return.** Each mutant is planted in memory at the head, and the named tests must go red:

| Mutant | Red |
|---|---|
| Cap ignored | RC1, RC2, RC4 |
| Cap with `rowid` order | RC3 rotation and RC1(b) |
| Oldest due first, without first-attempt priority | `test_a_new_incident_is_attempted_before_due_retries` and RC1(c) |
| A deferred job gets an event or an update | RC2 |
| `incident_key` tiebreak | The #628 regression (drafting probe: 8 red) |

**Return taxonomy.**
- **DONE:** every RC test recorded red at base and green at head; the regression, `test-ops`, `check` and the full suite are green, with records cited; the diff stays inside §5.
- **DONE_WITH_CONCERNS:** the selected outcome holds, with a disclosed baseline limitation unrelated to this patch that reproduces on unmodified origin/main.
- **NEEDS_CONTEXT:** a missing input, a contradicted default, or a #635 landing that overlaps §5's lines.
- **BLOCKED:** a necessary edit outside §5, or an environment failure the launcher cannot repair.

A failed required acceptance criterion is not DONE_WITH_CONCERNS.

**Verdict on H (§4):** RESOLVED when RC1-RC6 and the regression pass at the head and every listed mutant goes red. Any §4 falsifier observed makes H FALSIFIED.

## §7 — Acceptance checks (worker runs; coordinator (3) re-runs at the returned head)

```
python -I scripts/fp.py doctor
python -I scripts/fp.py python -m pytest tests/ops/test_book_incident_notifier_round_cap.py   # red at base, green at head
python -I scripts/fp.py python -m pytest tests/ops/test_book_incident_notifier.py             # unchanged: 59 passed
python -I scripts/fp.py test-ops
python -I scripts/fp.py check
python -I scripts/fp.py test                                                                  # full suite, before coordinator (3) acceptance
python -I scripts/fp.py python docs/notes/2026-09-29-s5-c3-record/stage1c-equivalence/stage1c_closure_table.py.txt . origin/main HEAD   # measured and staging: "changed": []
git diff --stat origin/main...HEAD                                                            # §5 files only
```

For each check, report the command, the interpreter, the head, and the printed `record.json` (`status: completed`, exit 0, `source_stable`). Disclose any pre-existing failure with its reproduction on unmodified origin/main (AGENTS.md `:220-227`).

**Full-suite carve-out.** Coordinator (3)'s dispatch relays a 2026-10-03 confirmation by Joshua in coordinator (3)'s chat: a code PR that needs coordinator (3)'s acceptance waits for the full suite. This card's author has not verified that relay. Coordinator (3) confirms it at freeze.

## §8 — Out of scope

- **Host wiring (TB-I3-HOST):** `BookHost`, its binding, the cap comparison, and HH7's measurement.
- **The host's values:** the cap, τ, W_j and T_n (OQ-HOST-4).
- **Channel binding (#635)** and any deploy, arming or provider traffic.
- **A retry-count cap.** OQ-2 is unchanged.
- **Deferral events or metrics,** and priority by `reason`.
- **Two processes on one journal** (#628 card §0.8 residual).
- **Naming the 5 s busy timeout as a constant.**

## §9 — Decisions and open questions

**Recorded.**
- **Authority.** Coordinator (3) dispatched this card under its #628 build authority (2026-10-03).
- **Full-suite carve-out.** Relayed and unverified (§7).

**OPEN.**
- **OQ-CAP-1** (coordinator (3)). Is the default 10? A lower default would need T22's configuration changed, and this card forbids editing that file. Lean: 10 (§0.5 item 3).
- **OQ-CAP-2** (coordinator (3)). The order. Lean: first attempts, then oldest due, then creation order (§0.5 item 2, §3.5). The alternative, oldest due with a `rowid` tiebreak, keeps the #628 suite green and an unconditional bound, but delays a new incident's first attempt behind due retries.
- **OQ-CAP-3** (coordinator (3), for #651's freeze). The notifier-side budget (§3.7). Two inputs for #651:
  - The journal-transaction count per `run_once` is 2 + 2·k·c, which #651 `:113` does not state.
  - Whether to count `COMMIT`'s lock wait.

  Once this card lands, #651 §0.5 item 6 (`:79`, "has no job cap") is stale.

## §10 — Audit hooks

```bash
python -I scripts/fp.py python scripts/check_brief.py --type handoff docs/briefs/handoffs/2026-10-03-notifier-round-job-cap-card-DRAFT.md
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-03-notifier-round-job-cap-card-DRAFT.md
git diff --stat 6e57fda origin/main -- ops/c1_rail/book_incident_notifier.py tests/ops/test_book_incident_notifier.py   # Expected at draft: empty
git grep -n book_incident_notifier origin/main -- ':!docs'     # Expected at draft: the module's test and the DURABLE_STORES path only
rg -n max_jobs_per_round ops/c1_rail/book_incident_notifier.py # Expected at head: field, validation, _CONFIG_KEYS, resolved(), publish_due
git diff origin/main...HEAD -- ops/c1_rail/book_incident_notifier.py | rg -n 'CHANNEL_KINDS|MAX_OUTSTANDING'   # Expected: no match
```

## §11 — GLM eligibility

**Not GLM-eligible. Opus/CC builds it.** This is incident-path code, the same basis as the #628 card's §11 (`:345-347`).

## §12 — Dispatch record

- **Status:** DRAFT. At freeze, coordinator (3) records:
  - the frozen revision;
  - the rulings on OQ-CAP-1 and OQ-CAP-2;
  - the #635 sequencing;
  - every moved anchor.
- **Executor (planned):** one Claude Code (Opus) worker session, seat worker, in a worktree under `.claude/worktrees/`. It works on a pushed `claude/*` branch, with no PR unless the coordinator records one.
- **Pre-dispatch checks:** the first two §10 hooks, run on the frozen file.
