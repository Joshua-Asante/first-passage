# Notifier follow-up: bounded rounds, ingestion, progress and no-rebuild open (TB-I3-HOST P7; #637, #651, #635 dependencies)

**Date:** 2026-10-03.
**Status:** **DRAFT.** Written under coordinator (3)'s #628 build authority. Coordinator (3) dispatched this docs-only rewrite on 2026-10-03 and owns the invariant table NF1-NF9 (§3). Other cards cite those names, so they are fixed. Coordinator (3) freezes this card (§12). Nothing here is dispatched.
**Base:** origin/main `04a86ac`. `git diff 6e679cc 04a86ac` is empty for `ops/c1_rail/`, `tests/ops/test_book_incident_notifier.py`, the #628 card and the HR spec, so anchors at `6e679cc` (the #628 merge) hold. Other heads read: #651 `af14556`, #637 `828ddda` and #635 `f4d1589`, all DRAFT. Their anchors hold only at those heads.
**Brief type:** CC handoff, code build (TDD) behind a named file boundary.
**Parent:** the #628 build card (`docs/briefs/handoffs/2026-10-02-book-incident-notifier-build-card.md`). Dependants:
- #651 P7 needs NF1, NF4, NF5, NF6 and NF8 before it freezes (`af14556:99`, `:113`).
- #637's notifier heartbeat marks on NF6 (`828ddda:9-10`).
- #635's D-MON-1 build needs NF7 and NF1-NF3 (P5, `f4d1589:99`).

**Findings being closed:**
1. `publish_due` runs one round for every due pending job, with no limit (`6e679cc:447-461`).
2. `poll` parses and re-INSERTs every owner row on every call (`:396-421`). The owner never deletes incidents: `book_account_owner.py` has no `DELETE` on `incidents`, and its insert is `INSERT OR IGNORE` (`:2091`). Ingestion therefore grows with no declared bound.
3. The notifier's only liveness signal is a clock value (`liveness()`, `:436-445`). A frozen or backward clock distorts it, and a pass that defers due work still refreshes it.
4. The constructor always rebuilds a faulty journal (`:284-291`). #635's record-delivery CLI therefore cannot open the live journal without risking a move-aside beside a running notifier (`f4d1589:141`).

**Selected outcome:** NF1-NF8 are built in `book_incident_notifier.py` and tested in a new file. NF9 stays unchanged.
**Ownership:** One Opus/CC worker builds it (§11). Coordinator (3) accepts it. Joshua merges.
**Return boundary:** A pushed `claude/*` branch that touches only §5's allowed files, or a precise blocker.

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
  - "Every red-first test in §6 (RC1-RC10) fails at the base revision and passes at the returned head; the failing-first run is recorded"
  - "Every §6 mutant turns its named tests red at the head"
  - "tests/ops/test_book_incident_notifier.py passes unchanged (59 tests at 6e679cc)"
  - "git diff --stat origin/main...HEAD lists only §5 allowed files, and the notifier diff stays inside §5's parts"
  - "python -I scripts/fp.py test-ops and python -I scripts/fp.py check: status completed, exit 0, source stable; or a pre-existing failure disclosed with its reproduction on unmodified origin/main"
  - "python -I scripts/fp.py test (full suite): recorded before coordinator (3) acceptance"
```

## §0 — Read first (report before writing code; otherwise `NEEDS_CONTEXT`)

| Input | Where | Read |
|---|---|---|
| Notifier (merged #628) | `ops/c1_rail/book_incident_notifier.py` at `6e679cc` | `ESCALATION_STEP_S` `:60-62`; `MAX_OUTSTANDING_PUBLISHES` `:63-66`; `CHANNEL_KINDS` `:67-70`; `_CONFIG_KEYS` `:74`; `jobs` columns `:77-80`; `NotifierConfig` `:205-256`; `__init__` `:266-291`; `_journal` `:295-319` (`mkdir` `:303`, `timeout=5` `:304`); `_journal_fault` `:321-341`; `_move_aside` `:343-361`; `_now` `:363-367`; `poll` `:396-421`; `run_once` `:425-436`; `liveness` `:438-445`; `publish_due` `:447-461`; `_publish_round` `:463-499`; `_transition` `:508-534`; `_refusal` `:536-552`; `_bounded_publish` `:554-580`; `record_delivery` `:612-626` |
| #628 tests (59) | `tests/ops/test_book_incident_notifier.py` | `Clock` `:59`; `_config` `:70`; `_notifier` `:80`; T17 (liveness) `:1138-1157`; `hanging` `:1199`; T22 `:1279` |
| #628 card | `docs/briefs/handoffs/2026-10-02-book-incident-notifier-build-card.md` | OQ-2 `:68`, `:322`; condition 3 rebuild `:86-90`; J0-J5 `:126-131`; forbidden list `:234-242`; §11 `:345-347` |
| HR spec | `docs/spec/2026-09-14-tb-s3-halt-resume-contract.md` | 60 s escalation `:63`; owner reading, condition (4) `:71`; backoff cap `:73` |
| TB-I3-HOST (#651) | `git show af14556:docs/briefs/handoffs/2026-10-03-tb-i3-host-heartbeat-wiring-card-DRAFT.md` | wrapper on `progress()` `:72`; §0.5 items 5-6 `:78-79`; P7 `:99`; `max_round_duration` `:113`; (b) `:118-121`; cap binding `:131`; HH7 `:198`; OQ-HOST-2 `:249`; OQ-CAP-3 `:254` |
| D-MON heartbeat (#637) | `git show 828ddda:docs/briefs/handoffs/2026-10-03-dmon-missed-heartbeat-monitor-card-DRAFT.md` | `:9-10` (the notifier pinger marks on NF6) |
| D-MON IRM binding (#635) | `git show f4d1589:docs/briefs/handoffs/2026-10-03-dmon-grafana-irm-binding-card-DRAFT.md` | `alert_uid` key `:65`; P5 `:99`; `CHANNEL_KINDS` entry `:117`; config file `:133`; retry interaction `:134`; CLI inputs `:137`; C3 item 3 `:141`; C4 `:145`; C5 `:146`; §5 `:160`; U15 `:198` |
| Owner | `ops/c1_rail/book_account_owner.py` | `incidents` table `:296`; `read_incidents` `:804-816` (`mode=ro`, `timeout=5`); insert `:2091` |
| Measured closures | `docs/notes/2026-09-29-s5-c3-record/stage1c-equivalence/stage1c_closure_table.py.txt`; `docs/briefs/handoffs/2026-09-24-tradeify-t00-p7-closure.md:630` | §2 |
| Rules | `AGENTS.md` *Python environment* `:220-227`, *Configuration as code* `:229-238`; `scripts/seat_authority.yml:105-108` | |

**The report states:** the dispatch revision; whether #635's D-MON-1 build has landed and which notifier lines it changed; whether #651 and #637 have frozen and which NF names they record; and every anchor that moved.

## §0.5 — Clarifications and recorded decisions

1. **Terms.**
   - A *pass* is one `publish_due` call. A *job round* is one `_publish_round`.
   - k is `max_jobs_per_round`, M is `max_retained_incidents`, n is the number of rows `read_incidents` returns, c is the channel count, and τ is `publish_timeout_s`.
   - L is #651's `max_notifier_loop_interval` (`af14556:113`): the longest gap between `run_once` starts.
2. **The "ever accepted" signal (checked against the code).** No `jobs` column records acceptance (`:77-80`).
   - After `poll`, `_transition` is the only writer of `rounds` and `channels_lost` (`:508-534`). It sets `channels_lost = 0` only when a round closes accepted by a delivering channel (`:482`, `:493-497`, `:530`). That close writes `provider_accepted` in the same transaction (`:491-492`).
   - So `rounds > 0 AND channels_lost = 0` holds exactly when the latest closed round was accepted. That is class A. Class U is `rounds = 0 OR channels_lost = 1`.
   - U contains every pending job that was never accepted. Its only other members are jobs that were accepted once but whose latest round lost every channel. NF2 places those in U.
   - Selection reads `jobs` columns only. It never scans `events`, which grows without bound.
   - Two cases stay in U: an acceptance known only from a `late_outcome` (J4 keeps round state), and an acceptance whose close never committed. Both keep the higher priority.
3. **Default k = 10 (probe).** An in-memory probe built NF1-NF4 and NF6: the cap, the class order, `cap_deferred`, the loud skip and the known-keys set. It ran the unchanged #628 suite at `04a86ac`, and no repo file changed.
   - k = 10: 59 passed.
   - k = 9: T22 (`test_a_hung_channel_cannot_take_the_healthy_channels_slot`, 10 due jobs in one pass) fails.
   - k = 1: 7 failed.
4. **D1 — NF5 cannot be done as written. Proposed change; coordinator (3) rules at freeze.**
   - The problem: if "at most `max_retained_incidents`" is an SQL `LIMIT M`, every pass drops the pending jobs above M by `rowid`, which are the newest incidents. They are never attempted and never counted as deferred, so the pass is not loud. That contradicts NF4's "nothing is dropped".
   - The change: this card reads every pending job.
   - The count still stays at most M while NF4's bound holds. Jobs come only from owner rows, one per key (`:413`), and the owner never deletes incidents, so pending ≤ jobs ≤ n ≤ M. Above M, NF4's event has already fired.
5. **D2 — how NF7 meets "creates nothing" (scope widening; coordinator (3) rules at freeze).**
   - `sqlite3.connect` creates a missing file (checked: a 0-byte file appears), and `_journal` creates the parent directory (`:303`).
   - An `is_file()` check alone leaves a race. A journal removed between that check and `_journal_fault`'s open (`:332`) would be created empty, then initialized.
   - The change: a `rebuild=False` instance opens every connection with the SQLite URI `Path(...).resolve().as_uri() + "?mode=rw"`, as `read_incidents` does with `mode=ro` (`book_account_owner.py:811`), and skips the `mkdir`. That open refuses a missing file (checked: `sqlite3.OperationalError`, which `_journal_fault` maps to `NotifierStoreError` at `:337-338`).
   - This touches the connect lines of `_journal` and `_journal_fault` (§5).
6. **An empty journal under `rebuild=False` follows NF7 as written.** A 0-byte file is not a `_journal_fault` fault (`:329-341`). The constructor initializes it, and `record_delivery` then refuses the key as unknown. #635 relies on this behavior (`f4d1589:141`).
7. **OQ-NF-1: owner reading, RULED.** The halt/resume owner, coordinator (2), wrote to coordinator (3) in a cross-session message on 2026-10-03: "OQ-NF-1: YES, with two conditions". This card records it from coordinator (3)'s dispatch. Its author has not seen the message, and coordinator (3) confirms the record at freeze.
   - The 60 s ruling (`ESCALATION_STEP_S`, `:60-62`; HR `:73`) binds class U only.
   - Class A may be deferred, because IRM already holds the alert and its own chain escalates.
   - Condition (1): a deferral is loud (NF3). Condition (2): class U is ordered by earliest due time (NF2).
8. **OQ-2 is unchanged.** It is a "no retry cap" rule (#628 card `:68`) and limits nothing per job. k limits jobs per pass.
9. **Digest.** `resolved()` gains two fields, so every configuration's digest changes.
   - `config_digest` is recorded per job and never compared, and no journal is deployed (#628 card `:90`).
   - #635's driver writes `resolved()` to `notifier-config.json`, and its CLI reads it back through `from_mapping` (`f4d1589:133`, `:137`). Both new keys must round-trip (RC10).
10. **Forbidden files** are §5's.

A contradicted default, a missing producer or a necessary edit outside §5 returns NEEDS_CONTEXT.

## §1 — Goal, scope, prerequisites

**Goal.**
- #651 can declare `max_round_duration` from NF8 and refuse a notifier whose cap differs (`af14556:113`, `:131`).
- #637's notifier heartbeat can mark on NF6 (`828ddda:10`).
- #635's CLI can open the live journal without rebuilding it (NF7).
- Every other #628 behavior stays as merged (NF9).

**Scope.** Two config fields, `poll`'s known-keys set and over-bound event, `publish_due`'s selection, cap and `cap_deferred`, `progress()`, the `rebuild` keyword, and one new test file.

| ID | Item | State at draft | Blocks |
|---|---|---|---|
| P1 | #628 merged | **Done** (`6e679cc`) | Nothing |
| P2 | Coordinator (3) rules on D1 and D2 (§0.5 items 4-5) and confirms the OQ-NF-1 record (item 7) | OPEN | Freeze |
| P3 | Sequencing with #635's D-MON-1 build (§5) | OPEN; recorded at dispatch | Dispatch |

## §2 — Measured-closure check

`book_incident_notifier.py` is in no measured closure. Checked at `04a86ac`:
- **S5 Stage 1c.** `stage1c_closure_table.py.txt . 04a86ac 04a86ac` lists 68 measured and 63 staging modules. The notifier is in neither list.
- **S5 records.** `git grep book_incident_notifier` over `docs/notes/2026-09-27-s5-part-a-measurement` and `docs/notes/2026-09-29-s5-c3-record` finds no match.
- **T00 P7 first-party closure** (40 modules, `2026-09-24-tradeify-t00-p7-closure.md:630`). The list is not in the repository. Static evidence instead: outside `docs/`, `git grep book_incident_notifier 04a86ac` matches only the module's own test and the path string in `scripts/check_durable_store_pragmas.py:54`. No module imports the notifier.

The worker re-runs the table from `origin/main` to `HEAD` (§7).

## §3 — Design: NF1-NF9 (names fixed by coordinator (3))

**NF1 — Cap.**
- Add `max_jobs_per_round: int = 10` to `NotifierConfig`, after `retry_max_s` (`:211`).
- `__post_init__` runs before the digest. It refuses a `bool`, any non-`int` (including `2.0`) and any value below 1 with `NotifierConfigError("max_jobs_per_round must be a positive integer")`.
- `_CONFIG_KEYS` (`:74`) gains the key, so `from_mapping` passes it through (`:248`), and `resolved()` emits it.
- `publish_due` runs at most k job rounds per call.
- A nominated job uses its slot whether or not its round publishes. A job closed between the snapshot and its admission (J2, `:470-473`) is not replaced. Replacing it would break NF8's transaction count.

**NF2 — Priority classes** (owner reading OQ-NF-1, §0.5 item 7).
- **Class U** is `rounds = 0 OR channels_lost = 1` (§0.5 item 2). It is ordered by `next_attempt_at` ascending, compared as parsed instants, then by `rowid` ascending.
- **Class A** is `rounds > 0 AND channels_lost = 0`: accepted, still pending, awaiting record-delivery (#635 `:134`). It uses the same order and comes after all of class U.
- The order is never newest-first. Newest-first can starve an older unaccepted incident while new ones keep arriving.
- **Normal-case guarantee.** Suppose every pass has at most k due class-U jobs. Then each due U job runs in the first pass in which it is due. Its attempts are at most `retry_max_s` + L apart by the journal's clock. With `retry_max_s` + L < 60 s, every 60 s escalation interval holds a retry. A pass with more than k due U jobs is loud (NF3), and owner condition (1) covers it.
- **Effective retry spacing** of a pending job X: at most `retry_max_s` + (⌊(A + N)/k⌋ + 1)·L.
  - A is the number of due jobs ahead of X in the NF2 order when X falls due. N is the number of incidents that sort ahead of X while it waits.
  - Class U, clock not stepping back: A counts the due U jobs ahead of X, and N = 0. A new job's due time is its poll time, never earlier than X's; on a tie, its larger `rowid` puts it behind X.
  - Class A: A counts every due U job plus the due A jobs ahead of X, and N counts every new incident (each starts in class U).
- **Starvation-freedom.** A round that ends without raising either finds the job closed (J2 or J3, where `_transition` writes nothing) or sets `next_attempt_at` = now_P + delay > now_P (`:522-530`). Here now_P is the time of the pass in which X was due and deferred.
  - A job that ran therefore sorts behind every job it overtook, and a deferred job is not written.
  - In each pass, X runs or k jobs ahead of it run, so X's rank falls by k each pass. Each new incident can pass X at most once.
  - Incidents are finite (one job per key), so every pending job runs.
- **A backward clock loosens the bound.** The caller supplies the clock; `_now` checks only that it is timezone-aware (`:363-367`), and #651 anticipates a backward step (`af14556:78`). A step back of B does two things:
  - X is not due until the clock again reaches its due time, which adds up to B.
  - An incident polled meanwhile can get a due time before X's. For class U, N then counts in the bound: ⌊(A + N)/k⌋.
  - Rotation still holds, because a re-run job and X are compared at the same now_P.
- **Wall-clock note.** Every event in a pass carries that pass's `now`. A job's publish can start up to `max_round_duration` after it, so publish starts can be that much further apart than the journal shows. Routed with OQ-CAP-3 (§9).

**NF3 — Loud deferral** (owner condition (1)).
- When the snapshot defers at least one due job, the pass writes one evidence event, `cap_deferred`. Its `incident_key` and `channel` are NULL, `at` is the pass's `now`, and its detail is `{unaccepted, accepted}`: counts of deferred due jobs per class, nothing else.
- The event is written in the snapshot transaction, so NF8's transaction count does not change.
- `publish_due` returns True when it deferred a due class-U job, and False otherwise.
- On True, `run_once` does not refresh `liveness()` and does not increment `progress()`, even though it completed. #637's notifier heartbeat stops marking, and the dead-man check pages after T_n (HR `:71`, condition 4).
- A pass that defers only class-A jobs still writes `cap_deferred`, but `liveness()` and `progress()` advance.
- **Post-rebuild backlog.** After a rebuild or first start, every retained incident becomes a `rounds = 0` job with the same due time (#628 card `:86-90`). A new incident waits behind them for up to ⌊A/k⌋ passes, and each of those passes is loud. For example, with 120 re-owed jobs, k = 10, and a new incident arriving before pass 2, the new incident's first attempt is in pass 13; passes 1-12 are loud.

**NF4 — Ingestion bound.**
- **Known keys.** A per-instance set is loaded once in the constructor's transaction, after the schema statements, with `SELECT incident_key FROM jobs` (every state). `poll` INSERTs only keys not in the set, still with `INSERT OR IGNORE`, so J1 is unchanged.
- The set is updated only after `poll`'s transaction commits, with the keys it inserted or found already present. A key added before `COMMIT` would be lost if the commit failed.
- Reading and parsing all n rows stays O(n). An owner-side incremental read is OQ-NF-2, out of scope (an owner packet).
- **Bound.** New field `max_retained_incidents: int = 1000`, validated like NF1, with the same exposure.
- When n (rows read this poll, malformed ones included) crosses from at-or-below M to above it, `poll` writes one evidence event, `retained_incidents_over_bound` `{count: n}`, in its transaction. The crossing state is per instance, starts at-or-below, and changes only after the commit.
- Processing continues, and nothing is dropped. NF8's bound assumes n ≤ M.
- **Residual R2.** The set assumes that only this instance fills and rebuilds the journal. If a second `rebuild=True` instance moved the journal aside, this instance would skip the re-owed keys; #628 would have re-inserted them. NF7 keeps #635's CLI from rebuilding. J0 serializes rounds per notifier only (#628 card `:126`); two notifier instances on one journal stay out of scope.

**NF5 — Pending fetch.**
- In the snapshot transaction, `publish_due` reads `rowid`, `incident_key`, `reason`, `detected_at`, `next_attempt_at`, `rounds` and `channels_lost` for every pending job (D1: no `LIMIT`; at most M while n ≤ M).
- "Due" is unchanged: `datetime.fromisoformat(next_attempt_at) <= now`, as at `:459`.
- The due jobs are sorted by (class, parsed `next_attempt_at`, `rowid`), and the first k are taken.
- Timestamps are never compared as SQL strings. ISO strings with different UTC offsets do not sort as instants, and a local-time clock produces both across a DST change.

**NF6 — Rollback-safe progress.**
- New `progress()` returns a per-instance int that starts at 0 and never decreases. It counts the `run_once` calls that completed without raising and without a loud pass.
- It is incremented exactly where `_last_loop_at` is set (`:436`), and a loud pass skips both together. `publish_due` and `poll` called alone change neither.
- `liveness()` keeps its contract apart from the NF3 skip, and its docstring says so.
- A heartbeat wrapper marks on an increase in `progress()`, never on a clock value (#651 `af14556:72`; #637 `828ddda:10`). A backward clock can move `liveness()` back; `progress()` never goes back.

**NF7 — No-rebuild open.**
- `IncidentNotifier.__init__` gains the keyword-only `rebuild=True`. True keeps today's behavior.
- With `rebuild=False`, a missing journal raises `NotifierStoreError` and creates no file or directory.
- With `rebuild=False`, a `_journal_fault` fault raises `NotifierStoreError`, with no `_move_aside` and no `journal_rebuilt` event.
- Every connection of a `rebuild=False` instance opens with `mode=rw` and skips the `mkdir` (D2). A journal removed after construction then fails instead of being created.
- An empty file is initialized as a fresh journal (§0.5 item 6). A hot rollback journal is rolled back by the writable open, as at `:333`, and nothing is moved.
- #635's CLI constructs with `rebuild=False` (`f4d1589:145`), which closes its pre-check-versus-constructor race (`:141`).

**NF8 — Whole-invocation bound.**

`run_once <= W_o + T_parse(n <= M) + (2 + 2·k·c)·W_j + k·c·τ + ε`

- W_o is the owner read's busy wait: 5 s (`book_account_owner.py:811-812`).
- T_parse(n) is the CPU time to read and parse n rows, then fetch, filter and sort at most n pending jobs.
- **2 + 2·k·c journal transactions** run on the pass thread: the poll, the snapshot (which holds `cap_deferred`), and one admission (`:470`) plus one close (`:486`) per (job, channel). A refused channel skips its close, and a closed job ends its round early; both only lower the count.
- W_j is each transaction's lock wait. `BEGIN IMMEDIATE` waits up to 5 s (`:304`). In the default rollback journal, `COMMIT` can wait another 5 s behind a reader, such as #635's read-only checks (`f4d1589:141`, `:146`), so W_j can reach 10 s.
- A run makes at most k·c bounded publishes, each waiting at most τ (`join`, `:575`).
- ε is fsync and other CPU time, which no declared bound covers. HH7 measures it (`af14556:198`).
- Late-outcome threads contend for the same lock; that wait is inside W_j.
- **At #628's defaults** (τ = 10 s, c = 2) and k = 1, the bound is 5 + 6·5 + 20 = 55 s, or 85 s with W_j = 10 s, before T_parse. On the notifier side, #651's condition (b) needs `max_round_duration` below 30 s at the lean T_n = 60 s (`af14556:118-121`, `:254`). So OQ-CAP-3 goes to #651's freeze: choose τ, the declared W_j, k or T_n.

**NF9 — Unchanged.**
- J0-J5 (#628 card `:126-131`) and backoff (`:522-530`).
- The payload, its idempotency key, and #635's rule that this key is the `alert_uid` (`f4d1589:65`).
- `MAX_OUTSTANDING_PUBLISHES`, its reservation, and one live publish per (job, channel) pair (`_refusal`, `:536-552`).
- `record_delivery` and the delivery paths: `_publish_round` after nomination, `_bounded_publish`, `_record_late` and `_transition`.
- `CHANNEL_KINDS`, which is #635's line.
- `tests/ops/test_book_incident_notifier.py` passes unchanged.

## §4 — Hypothesis and falsifier

**H:** With NF1-NF8 built:
- each pass runs at most k jobs, in the NF2 order;
- a pass that defers a due class-U job is loud;
- `poll` inserts only new keys;
- `progress()` counts only clean, non-loud loops;
- `rebuild=False` never creates a journal or moves one aside;
- one `run_once` stays within NF8's counts;
- and NF9 holds.

**Falsifier.** Any one of these refutes H:
- a pass that runs more than k jobs, or that refills the slot of a closed nominated job;
- a class-A job running before a due class-U job, or class U out of (due time, `rowid`) order;
- under persistent failure, a due job that does not run within NF2's bound;
- a pass that defers a due class-U job yet refreshes `liveness()` or advances `progress()`;
- a class-A-only deferral that stops `liveness()` or `progress()`;
- more than one `cap_deferred` in a pass, or counts that differ from the deferred jobs;
- an INSERT for a known key, or a key lost after a failed `poll` commit;
- `retained_incidents_over_bound` written other than once per crossing;
- a pending job above M that is never attempted;
- `progress()` decreasing, or changing on a `run_once` that raises or is loud;
- `rebuild=False` creating a file or directory, moving a journal aside or writing `journal_rebuilt`;
- a `run_once` with more than 2 + 2·k·c journal transactions, more than k·c publishes, or more than one owner read;
- any #628 test failing, or a change to an NF9 item;
- a configuration that accepts 0, a negative value, a `bool` or a non-`int` for either new field, or that fails the `resolved()`/`from_mapping` round trip.

## §5 — Files

**Allowed:**
- `ops/c1_rail/book_incident_notifier.py`, **only** these parts:
  - `_CONFIG_KEYS` (`:74`);
  - the two `NotifierConfig` fields, their validation and their `resolved()` entries (`:205-256`);
  - `__init__` (`:266-291`): the `rebuild` keyword, the known-keys load, and the progress and crossing state;
  - the connect lines of `_journal` (`:302-304`) and `_journal_fault` (`:332`), through one new private helper (D2);
  - `poll` (`:396-421`): the known-keys filter and the over-bound event;
  - `run_once` (`:425-436`), the `liveness` docstring (`:438-445`), and a new `progress()` beside them;
  - `publish_due` and its docstring (`:447-461`);
  - the module docstring's condition (4) sentence (`:19-20`), to name `progress()`.
- `tests/ops/test_book_incident_notifier_followup.py` (new).
- This card, for the freeze commit and the executor return only.

**Forbidden (stop and return if a change seems needed):**
- Every other line of `book_incident_notifier.py`, including:
  - `ESCALATION_STEP_S` (`:60-62`) and `MAX_OUTSTANDING_PUBLISHES` (`:63-66`);
  - `CHANNEL_KINDS` and its comment (`:67-70`), which #635's D-MON-1 worker owns (`f4d1589:160`);
  - the journal schema (`:76-84`) and `_move_aside`;
  - `_publish_round`, `_pending`, `_transition`, `_refusal`, `_bounded_publish`, `_record_late`, `record_delivery` and the read methods.
- `tests/ops/test_book_incident_notifier.py` and every other existing test.
- These files:
  - `book_account_owner.py` and every other `ops/c1_rail/book_*.py`;
  - `scripts/check_durable_store_pragmas.py`;
  - `ops/c1_signal_daemon/**`, including #651's `book_host.py` and #637's `book_heartbeat.py`.
- Everything the #628 card forbids (`:234-242`).
- The #628, #635, #637 and #651 cards.

**Sequencing with #635's D-MON-1 build.**
- **This card lands first** (#635 P5, `f4d1589:99`; #651 P7). #635 then re-anchors. Its §5 edits only the `CHANNEL_KINDS` entry and its comment (`f4d1589:160`). The nearest hunk here is at `:74`, with `:71-73` unchanged between them, so the hunks are disjoint.
- #635's driver and CLI round-trip `resolved()` through `from_mapping` (`:133`, `:137`), so they consume both new keys (§0.5 item 9).
- If D-MON-1 lands first anyway, this worker merges current main, re-reads the anchors and keeps the same hunks. Neither worker edits the other's lines.

## §6 — Red-first tests and return taxonomy

**Test file.** The tests go in `tests/ops/test_book_incident_notifier_followup.py`.
- They feed synthetic incident rows through an injected `read_incidents`, or use a real `BookAccountOwner` as #628 does. They use a fake notifier clock and `FakeChannel` or small subclasses of it.
- The file defines its own helpers and does not import the #628 test module.
- RC2, RC5 and RC9 may seed job state with direct `UPDATE`s of `state`, `rounds`, `channels_lost` and `next_attempt_at` in the test's own journal.
- **Run the file at base first and record the failures.** The fields and the keyword are absent at base. RC10 asserts the field's name in the error message, so `from_mapping`'s base refusal ("unknown notifier config keys") does not satisfy it.

| ID | Test | Basis |
|---|---|---|
| RC1 | `test_cap_admits_exactly_k`. (a) Five never-attempted due jobs, k = 2, a delivering channel: the passes attempt [1,2], then [3,4], then [5]. (b) k = 2 and three due jobs, where the channel's publish of job 1 calls `record_delivery` for job 2. Job 2 gets no `attempt` (J2), and job 3 is not attempted in that pass. That pass's `cap_deferred` is `{unaccepted: 1, accepted: 0}` | NF1 |
| RC2 | `test_class_u_by_earliest_due_then_class_a`. One pass, k = 8, a delivering channel, seeded due jobs. Class U: `rounds = 0` at t−40 and t−30, `channels_lost = 1` at t−45 and t−35, and two `rounds = 0` jobs that share t−20. Class A: t−60 and t−50. Expected attempt order: t−45, t−40, t−35, t−30, the t−20 pair by `rowid`, then t−60 and t−50. A second case uses two U jobs whose `next_attempt_at` strings carry different UTC offsets and sort the other way as text: the earlier instant runs first | NF2, NF5 |
| RC3 | `test_rotation_within_a_class_under_persistent_failure`. (a) Class U: five jobs, k = 2, a channel that always rejects, and the clock advanced 60 s (more than `retry_max_s`) before each pass. The attempted sets are {1,2}, {3,4}, {5,1}, {2,3}, {4,5}, {1,2}, and every job runs in any three consecutive passes. (b) Class A: three jobs, k = 1, a channel that accepts without delivery, and the same clock. Passes 4-9 run jobs 1, 2, 3, 1, 2, 3 | NF2 |
| RC4 | `test_post_rebuild_backlog_is_loud_and_earliest_due_first`. A journal of unreadable bytes and `rebuild=True` (`journal_rebuilt` written). `read_incidents` returns 120 rows, k = 10, a delivering channel, and the clock advances 1 s per pass. Pass 1 attempts the 10 lowest `rowid`s and writes `cap_deferred` `{110, 0}`; afterwards `progress() == 0` and `liveness() is None`. A 121st incident is committed before pass 2, and its first attempt is in pass 13, after every re-owed job. Passes 1-12 are each loud, with one `cap_deferred` each (`unaccepted` 110, 101, 91, …, 1). Pass 13 is not loud: `progress() == 1`, and `liveness()` equals pass 13's clock. The test asserts state and order, not elapsed time | NF2, NF3 |
| RC5 | `test_cap_deferred_once_per_pass_with_counts_and_loudness`. (a) Seeded due jobs, 3 in class U and 2 in class A, k = 2: exactly one `cap_deferred`, `{unaccepted: 1, accepted: 2}`, with exactly those two detail keys. The `run_once` is loud: `progress()` and `liveness()` are unchanged. (b) Only 3 due class-A jobs, k = 2: `{unaccepted: 0, accepted: 1}`, and the pass is not loud (`progress()` + 1, `liveness()` = the clock). (c) A pass with at most k due jobs writes no `cap_deferred` | NF3 |
| RC6 | `test_known_keys_and_retained_bound`. Statements are traced by a wrapper around `_journal` that calls `set_trace_callback` on the yielded connection. (a) A second `poll` over the same rows executes no INSERT into `jobs`; a new row adds exactly one; a fresh instance on the same journal inserts none. (b) A `poll` whose transaction fails (a patched `_event` raises `sqlite3.OperationalError` on `detected`) raises `NotifierStoreError`, and the next `poll` inserts that key. (c) With M = 3, polls over 2, 4, 5, 3 and 4 rows write `retained_incidents_over_bound` exactly twice, `{count: 4}` each time, and every row has a job. (d) With M = 3, k = 5 and five due pending jobs, all five are attempted in one pass | NF4, NF5 (D1) |
| RC7 | `test_progress_counts_clean_non_loud_loops_only`. `progress()` is 0 at construction and rises by 1 per clean `run_once`. It does not change on a `run_once` that raises (a raising `read_incidents`; a journal replaced by a directory, as T17 does) or on a loud pass. With the clock stepped back 1 h between clean loops, `liveness()` moves back while `progress()` still rises by 1 | NF6 |
| RC8 | `test_rebuild_false_refuses_missing_and_faulty_journals`. (a) A missing path inside a missing directory: `NotifierStoreError`, and the listing of `tmp_path` is unchanged. (b) The race: `Path.is_file` patched to report True for a missing path still raises and creates nothing. (c) Unreadable bytes, a failed integrity check and a foreign schema: each raises; the file bytes, any sidecars and the listing are unchanged; no `*.corrupt-*` file and no `journal_rebuilt`. (d) A valid journal constructs, and `record_delivery` closes a job. With `rebuild=True`, the faulty files of (c) are still moved aside | NF7 |
| RC9 | `test_run_once_stays_within_nf8_counts`. `read_incidents` returns M = 50 rows, all already journaled: 45 seeded delivered and 5 due pending. k = 2, and c = 2 channels that both reject at once. On the pass thread: `read_incidents` is called once; INSERTs into `jobs` = 0; `_journal` is entered exactly 2 + 2·k·c = 10 times, with `cap_deferred` inside the snapshot transaction; `_bounded_publish` is called exactly k·c = 4 times. The parse time for M rows is printed for the return, not asserted | NF8 |
| RC10 | `test_new_fields_validated_and_round_trip[max_jobs_per_round, max_retained_incidents]`. Each of 0, -1, True, False, 1.0, 2.5, "2" and None raises `NotifierConfigError` naming the field, through `NotifierConfig(...)` and through `from_mapping`. The defaults 10 and 1000 appear in `resolved()`. For the defaults and for (3, 7), `from_mapping(c.resolved()) == c` with equal digests. Changing either field changes the digest | NF1, NF4 |
| — | Regression: `tests/ops/test_book_incident_notifier.py` passes unchanged (59) | NF9 |

**Mutant evidence for the return.** Each mutant is planted in memory at the head, and the named tests must go red:

| Mutant | Red |
|---|---|
| Cap ignored | RC1, RC4, RC9 |
| A closed nominated job's slot refilled | RC1(b) |
| Newest first within class U | RC2, RC4 |
| First attempts before lost jobs (this card's previous order) | RC2 |
| One queue with no classes | RC2, RC5 |
| `next_attempt_at` compared as text | RC2 |
| Plain `rowid` order under the cap | RC3(a) |
| A loud pass refreshes `liveness()` or `progress()` | RC4, RC5, RC7 |
| A class-A-only deferral is loud | RC5(b) |
| `cap_deferred` in its own transaction | RC9 |
| Known keys ignored | RC6(a), RC9 |
| Known set updated before `COMMIT` | RC6(b) |
| `retained_incidents_over_bound` on every poll above M | RC6(c) |
| `LIMIT M` on the pending fetch | RC6(d) |
| `progress()` derived from the clock | RC7 |
| `rebuild` ignored; an `is_file` check without `mode=rw` | RC8(a)-(c); RC8(b) |
| An `incident_key` tiebreak | The #628 regression |

**Return taxonomy.**
- **DONE:** every RC test recorded red at base and green at head; every mutant red; the regression, `test-ops`, `check` and the full suite green, with records cited; the diff inside §5.
- **DONE_WITH_CONCERNS:** the selected outcome holds, with a disclosed baseline limitation unrelated to this patch that reproduces on unmodified origin/main.
- **NEEDS_CONTEXT:** a missing input, a contradicted default, D1 or D2 ruled against, or a #635 landing that overlaps §5's parts.
- **BLOCKED:** a necessary edit outside §5, or an environment failure the launcher cannot repair.

A failed required acceptance criterion is not DONE_WITH_CONCERNS.

**Verdict on H (§4):** RESOLVED when RC1-RC10 and the regression pass at the head and every listed mutant goes red. Any §4 falsifier observed makes H FALSIFIED.

## §7 — Acceptance checks (worker runs; coordinator (3) re-runs at the returned head)

```
python -I scripts/fp.py doctor
python -I scripts/fp.py python -m pytest tests/ops/test_book_incident_notifier_followup.py   # red at base, green at head
python -I scripts/fp.py python -m pytest tests/ops/test_book_incident_notifier.py            # unchanged: 59 passed
python -I scripts/fp.py test-ops
python -I scripts/fp.py check
python -I scripts/fp.py test                                                                 # full suite, before coordinator (3) acceptance
python -I scripts/fp.py python docs/notes/2026-09-29-s5-c3-record/stage1c-equivalence/stage1c_closure_table.py.txt . origin/main HEAD   # measured and staging: "changed": []
git diff --stat origin/main...HEAD                                                           # §5 files only
```

For each check, report the command, the interpreter, the head, and the printed `record.json` (`status: completed`, exit 0, `source_stable`). Disclose any pre-existing failure with its reproduction on unmodified origin/main (AGENTS.md `:220-227`).

**Full suite.** Joshua confirmed on 2026-10-03, directly to coordinator (3), that a code PR needing coordinator (3)'s acceptance waits for the full suite. This card records that from coordinator (3)'s dispatch; its author has not seen the confirmation.

## §8 — Out of scope

- **Host wiring (#651):** `BookHost`, its binding, the cap comparison, and HH7's measurement.
- **The host's values:** k, M, τ, W_j, L and T_n (OQ-HOST-4, OQ-CAP-3).
- #635's channel and CLI, #637's heartbeat, and any deploy, arming or provider traffic.
- **OQ-NF-2:** an owner-side incremental read.
- **A retry-count cap.** OQ-2 is unchanged.
- Per-job handling of a deterministic raise (R1).
- Two notifier instances on one journal.
- Naming the 5 s busy timeouts as constants.

## §9 — Decisions, residuals and open questions

**Recorded.**
- **Authority.** Coordinator (3) dispatched this rewrite under its #628 build authority on 2026-10-03.
- **OQ-NF-1:** owner reading, RULED (§0.5 item 7).
- **Full-suite rule** (§7).

**Residuals.**
- **R1. A deterministic raise in a round.** An example is `assert_no_secrets` rejecting a job's reason (`:464`; `c1_rail_telemetry.py:127-144`).
  - The job stays at `rounds = 0` with its due time unchanged, so it remains the earliest-due class-U job. It heads every pass and blocks every job behind it. Under `rowid` order it blocked only later rows.
  - It is loud: `run_once` raises, so `liveness()` and `progress()` stop.
  - It is latent: owner reasons are codes or canonical JSON.
- **R2. Known keys versus an outside rebuild** (NF4).
- **R3. A backward clock** loosens NF2's bound (NF2).
- **R4. pending ≤ n.** D1's bound assumes one owner DB feeds the journal and never deletes incidents. Replacing the owner DB under an existing journal breaks it.
- **R5. Wall-clock spacing** can exceed the journal's spacing by up to `max_round_duration` (NF2).

**OPEN.**
- **D1** (coordinator (3)). NF5 without `LIMIT` (§0.5 item 4). Lean: accept.
- **D2** (coordinator (3)). NF7's `mode=rw` open, which widens §5 to the connect lines (§0.5 item 5). Lean: accept.
- **OQ-NF-2** (the `book_account_owner.py` owner). An incremental `read_incidents`. Out of scope.
- **OQ-CAP-3** (coordinator (3), for #651's freeze). Choose τ, W_j, k or T_n so that NF8 stays below 30 s, and account for R5. Once this card lands, #651 §0.5 item 6 (`af14556:79`, "has no job cap") is stale.

## §10 — Audit hooks

```bash
python -I scripts/fp.py python scripts/check_brief.py --type handoff docs/briefs/handoffs/2026-10-03-notifier-round-job-cap-card-DRAFT.md
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-03-notifier-round-job-cap-card-DRAFT.md
git diff --stat 6e679cc origin/main -- ops/c1_rail/book_incident_notifier.py tests/ops/test_book_incident_notifier.py   # Expected at draft: empty
git grep -n book_incident_notifier origin/main -- ':!docs'       # Expected at draft: the module's test and the DURABLE_STORES path only
git grep -n -i 'delete from incidents' origin/main -- ops        # Expected: no match (D1's pending <= n)
rg -n 'max_jobs_per_round|max_retained_incidents|cap_deferred|retained_incidents_over_bound|def progress|rebuild' ops/c1_rail/book_incident_notifier.py   # Expected at head: fields, validation, _CONFIG_KEYS, resolved(), poll, publish_due, progress, __init__
git diff origin/main...HEAD -- ops/c1_rail/book_incident_notifier.py | rg -n 'CHANNEL_KINDS|MAX_OUTSTANDING|ESCALATION_STEP'   # Expected: no match
```

## §11 — GLM eligibility

**Not GLM-eligible. Opus/CC builds it.** This is incident-path code, on the same basis as the #628 card's §11 (`:345-347`).

## §12 — Dispatch record

- **Status:** DRAFT. At freeze, coordinator (3) records:
  - the frozen revision;
  - the rulings on D1 and D2, and confirmation of the OQ-NF-1 record;
  - the #635 sequencing;
  - every moved anchor.
- **Executor (planned):** one Claude Code (Opus) worker session, seat worker, in a worktree under `.claude/worktrees/`. It works on a pushed `claude/*` branch, with no PR unless the coordinator records one.
- **Pre-dispatch checks:** the first two §10 hooks, run on the frozen file.
