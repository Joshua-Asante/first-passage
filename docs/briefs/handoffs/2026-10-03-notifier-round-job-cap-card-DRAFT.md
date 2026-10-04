# Notifier follow-up: bounded rounds, ingestion, progress and no-rebuild open (TB-I3-HOST P7; #637, #651, #635 dependencies)

**Date:** 2026-10-03.
**Status:** **DRAFT.** Written under coordinator (3)'s #628 build authority. Coordinator (3) dispatched this docs-only rewrite on 2026-10-03 and owns the invariant table NF1-NF9 (§3). Other cards cite those names, so they are fixed. Coordinator (3) freezes this card (§12). Nothing here is dispatched.
**Fold (2026-10-03):** the review of `7da0288` (two P2, three P3) is folded, and coordinator (3)'s card-owner rulings on D1, D2 and the `rebuild=False` empty-journal refusal are recorded (§0.5 items 4-6). The review of `5d2356c` (two P3, one nit) is folded. OQ-NF-3 is RULED (a), the first-page reading, which supersedes the earlier sizing condition (§0.5 item 11); the halt-sequence key is §0.5 item 12. The review of `4990ce7` (one P2 and three P3 on this card) is resolved or retired in §0.5 item 11 and §9. The review of `0c56d35` (two P2, five P3) is folded under coordinator (3)'s card-owner rulings of 2026-10-03: (a) tiers inside class U (NF2), (b) three readings of the OQ-NF-3 ruling, recorded PENDING coordinator (2)'s confirmation (§0.5 item 11, R6), and (c) a k floor of 8.
**Base:** origin/main `04a86ac`. `git diff 6e679cc 04a86ac` is empty for `ops/c1_rail/`, `tests/ops/test_book_incident_notifier.py`, the #628 card and the HR spec, so anchors at `6e679cc` (the #628 merge) hold. Other heads read: #651 `fb3c3ba`, #637 `828ddda` and #635 `f4d1589`, all DRAFT. Their anchors hold only at those heads.
**Brief type:** CC handoff, code build (TDD) behind a named file boundary.
**Parent:** the #628 build card (`docs/briefs/handoffs/2026-10-02-book-incident-notifier-build-card.md`). Dependants:
- #651 P7 needs NF1, NF3, NF4, NF5, NF6 and NF8 before it freezes (`fb3c3ba:99`, `:113`).
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
| HR spec | `docs/spec/2026-09-14-tb-s3-halt-resume-contract.md` | 60 s escalation `:63`; owner reading, condition (4) `:71`; backoff cap `:73`; INTERVENTION dispatch `:26`; omission detectors `:115`; C-a incident rows `:150-156`; other legs `:164`; R-T9 cases `:174`; durable resume owner and no resume `:203-204` |
| TB-I3-HOST (#651) | `git show fb3c3ba:docs/briefs/handoffs/2026-10-03-tb-i3-host-heartbeat-wiring-card-DRAFT.md` | wrapper on `progress()` `:72`; §0.5 items 5-6 `:78-79`; P7 `:99`; `max_round_duration` `:113`; (b) `:119-122`; (d) `:123`; (e') `:124`; cap binding `:136`; `validate_binding` `:137`; `ESCALATION_STEP_S` restated `:138`; import ban `:151`; HH4 `:200`; HH7 `:203`; OQ-HOST-2 `:254`; OQ-CAP-3 `:259` |
| D-MON heartbeat (#637) | `git show 828ddda:docs/briefs/handoffs/2026-10-03-dmon-missed-heartbeat-monitor-card-DRAFT.md` | `:9-10` (the notifier pinger marks on NF6) |
| D-MON IRM binding (#635) | `git show f4d1589:docs/briefs/handoffs/2026-10-03-dmon-grafana-irm-binding-card-DRAFT.md` | `alert_uid` key `:65`; P5 `:99`; `CHANNEL_KINDS` entry `:117`; config file `:133`; retry interaction `:134`; CLI inputs `:137`; C3 item 3 `:141`; C4 `:145`; C5 `:146`; §5 `:160`; U15 `:198` |
| Owner | `ops/c1_rail/book_account_owner.py` | `incidents` table `:296`; `read_incidents` `:804-816` (`mode=ro`, `timeout=5`); insert `:2091`; `barrier-expired` `:1123`; attempt- and fact-keyed incident ids `:1906`, `:2116-2283` |
| Halt sizing and key (§0.5 items 11-12) | `docs/notes/2026-09-26-close-semantics-c-a.md`; `ops/c1_rail/book_policy.py`; `ops/c1_rail/book_account_owner.py`; `ops/c1_rail/book_bootstrap.py`; `ops/c1_rail/book_migration.py` | O1 `:411`; O2b `:413`; O3 `:414`; O4-O8 `:415-419`; O9 `:420`; `BOOK_LEGS` `:179-197`; owner `_SCHEMA` incidents `:296-297`, restart `:445`, `owner_state` singleton `:718-720`, scheduled exit `:1963-1969`, flatten `:1993-2003`, `own-flat-deadline` `:2009-2017`, `_halt_db` `:2088-2094`; bootstrap `:137-141`, `:174`; migration `:412` |
| Measured closures | `docs/notes/2026-09-29-s5-c3-record/stage1c-equivalence/stage1c_closure_table.py.txt`; `docs/briefs/handoffs/2026-09-24-tradeify-t00-p7-closure.md:630` | §2 |
| Rules | `AGENTS.md` *Python environment* `:220-227`, *Configuration as code* `:229-238`; `scripts/seat_authority.yml:105-108` | |

**The report states:** the dispatch revision; whether #635's D-MON-1 build has landed and which notifier lines it changed; whether #651 and #637 have frozen and which NF names they record; and every anchor that moved.

## §0.5 — Clarifications and recorded decisions

1. **Terms.**
   - A *pass* is one `publish_due` call. A *job round* is one `_publish_round`.
   - k is `max_jobs_per_round`, M is `max_retained_incidents`, n is the number of rows `read_incidents` returns, c is the channel count, and τ is `publish_timeout_s`.
   - L is #651's `max_notifier_loop_interval` (`fb3c3ba:113`): the longest gap between `run_once` starts. This card keeps that definition rather than redefining L between `publish_due` times, because L is #651's declared binding value.
   - poll_bound = W_o + T_parse(M) + W_j (NF8's terms): the longest `poll`, which separates a `run_once` start from its `publish_due` `now`. Attempts carry that `now`, so m consecutive passes span at most m·L + poll_bound of journal time.
2. **The "ever accepted" signal (checked against the code).** No `jobs` column records acceptance (`:77-80`).
   - After `poll`, `_transition` is the only writer of `rounds` and `channels_lost` (`:508-534`). It sets `channels_lost = 0` only when a round closes accepted by a delivering channel (`:482`, `:493-497`, `:530`). That close writes `provider_accepted` in the same transaction (`:491-492`).
   - So `rounds > 0 AND channels_lost = 0` holds exactly when the latest closed round was accepted. That is class A. Class U is `rounds = 0 OR channels_lost = 1`.
   - U contains every pending job that was never accepted. Its only other members are jobs that were accepted once but whose latest round lost every channel. NF2 places those in U.
   - Selection reads `jobs` columns only. It never scans `events`, which grows without bound.
   - Two cases stay in U: an acceptance known only from a `late_outcome` (J4 keeps round state), and an acceptance whose close never committed. Both keep the higher priority.
3. **The #628 suite and k (probe).** An in-memory probe built NF1-NF4 and NF6: the cap, the class order, `cap_deferred`, the loud skip and the known-keys set. It ran the unchanged #628 suite at `04a86ac`, and no repo file changed.
   - k = 10: 59 passed.
   - k = 9: T22 (`test_a_hung_channel_cannot_take_the_healthy_channels_slot`, 10 due jobs in one pass) fails.
   - k = 1: 7 failed.
   - So 10 is the smallest cap that keeps T22. It is the default (item 11).
   - Re-probed on 2026-10-03 with NF2's order (items 11-12) added, in memory, on the unchanged #628 code and suite at `7e409df` (`git diff 4990ce7 7e409df` is empty for `ops/c1_rail` and the suite). With ruling (a)'s tiers: k = 10, 59 passed; k = 9, T22 fails; k = 1, 7 failed. The earlier two-tier order gave the same at k = 10 and 9. The 59 stay an acceptance check.
4. **D1 — NF5 reads every pending job, with no SQL `LIMIT`. RULED by coordinator (3), card owner, 2026-10-03.**
   - The problem: if "at most `max_retained_incidents`" is an SQL `LIMIT M`, every pass drops the pending jobs above M by `rowid`, which are the newest incidents. They are never attempted and never counted as deferred, so the pass is not loud. That contradicts NF4's "nothing is dropped".
   - The ruling: read every pending job. RC6(d) guards it.
   - The count still stays at most M while NF4's bound holds. Jobs come only from owner rows, one per key (`:413`), and the owner never deletes incidents, so pending ≤ jobs ≤ n ≤ M. Above M, NF4's event has already fired.
   - NF2's sequences (item 12) widen the read to every job, in every state; jobs ≤ n bounds it the same way.
5. **D2 — how NF7 meets "creates nothing". RULED by coordinator (3), card owner, 2026-10-03.**
   - `sqlite3.connect` creates a missing file (checked: a 0-byte file appears), and `_journal` creates the parent directory (`:303`).
   - An `is_file()` check alone leaves a race. A journal removed between that check and `_journal_fault`'s open (`:332`) would be created empty by that open. Item 6 would then refuse it, but the file would already exist, which breaks "creates nothing".
   - The ruling: a `rebuild=False` instance opens every connection with the SQLite URI `Path(...).resolve().as_uri() + "?mode=rw"`, as `read_incidents` does with `mode=ro` (`book_account_owner.py:811`), and skips the `mkdir`. That open refuses a missing file (checked: `sqlite3.OperationalError`, which `_journal_fault` maps to `NotifierStoreError` at `:337-338`).
   - §5's allowed parts widen to the `_journal` connect lines (`:302-304`) and the `_journal_fault` connect (`:332`).
6. **Empty, table-less or foreign-schema journal under `rebuild=False`: REFUSE. RULED by coordinator (3), card owner, 2026-10-03.** This supersedes this card's earlier "initialize an empty journal".
   - Any schema other than `_JOURNAL_SCHEMA` (`:88-102`), including an empty or table-less file, raises `NotifierStoreError`, and nothing is initialized (NF7).
   - Why: a journal removed under a running notifier is re-created with no tables by that notifier's next open (`:303-304`). If another open then initialized it, the running instance's known-keys set (NF4) would skip every owed key; the review's probe saw 3 pending jobs become 0 while `progress()` advanced. Refused, the running instance keeps raising, which is loud (RC8(f), R2).
   - #635 is unaffected. Its CLI pre-check already refuses an empty file (`f4d1589:141`, C3 item 3), and a constructor refusal exits non-zero like any `NotifierStoreError`. Its `:141` sentence that the constructor initializes an empty file describes the superseded behavior but does not say the CLI relies on it, so its wording needs no change here.
7. **OQ-NF-1: owner reading, RULED.** The halt/resume owner, coordinator (2), wrote to coordinator (3) in a cross-session message on 2026-10-03: "OQ-NF-1: YES, with two conditions". **Confirmed by coordinator (3):** the message is genuine and is recorded in coordinator (3)'s log (AUTH: coordinator (3)'s 2026-10-03 fold dispatch).
   - The 60 s ruling (`ESCALATION_STEP_S`, `:60-62`; HR `:73`) binds class U only.
   - Class A may be deferred, because IRM already holds the alert and its own chain escalates. While class-U load fills the cap, that deferral has no bound and is not loud (NF2, NF3); this reading permits it.
   - Condition (1): a deferral is loud (NF3). Condition (2): class U is ordered by earliest due time (NF2).
   - OQ-NF-3's first-page reading (item 11) narrows the 60 s binding inside class U to representatives and orders them first, first jobs ahead of later-job representatives (NF2; ruling (a), item 11).
8. **OQ-2 is unchanged.** It is a "no retry cap" rule (#628 card `:68`) and limits nothing per job. k limits jobs per pass.
9. **Digest.** `resolved()` gains two fields, so every configuration's digest changes.
   - `config_digest` is recorded per job and never compared, and no journal is deployed (#628 card `:90`).
   - #635's driver writes `resolved()` to `notifier-config.json`, and its CLI reads it back through `from_mapping` (`f4d1589:133`, `:137`). Both new keys must round-trip (RC10).
10. **Forbidden files** are §5's.
11. **OQ-NF-3: RULED (a), the first-page reading,** by the halt/resume owner, coordinator (2), 2026-10-03 (AUTH: coordinator (3)'s 2026-10-03 fold dispatch). It supersedes the same day's sizing condition, "Size k >= the maximum number of unaccepted jobs one halt can produce" (`4990ce7` §0.5 item 11). The ruling:
   > "The 60 s retry guarantee binds: the oldest due class-U job of each halt sequence; any job whose halt sequence does not yet have an accepted page. The purpose ... is that Joshua is engaged within the escalation window for every halt. Once one page per halt sequence is accepted, IRM's own chain carries the escalation, and later incidents add context to a halt that is already attended."
   - **Readings (coordinator (3)'s, PENDING coordinator (2)'s confirmation, which coordinator (3) has requested; P4, §1).** NF2's 60 s scope rests on them until confirmed.
     - (i) "Oldest due" is the earliest `next_attempt_at`.
     - (ii) Clause (i) applies only to sequences without an accepted page.
     - (iii) Clause (ii) is read per sequence: one representative retry per unpaged sequence in each 60 s window. In a burst above k, an unpaged sequence's non-representative jobs fall under the residual's "(and any sequence without an accepted page)" (R6).
   - **Condition (1), scheduling.** Within the unaccepted class, a halt sequence's first job is scheduled ahead of that sequence's later jobs. Across sequences, order is by earliest due time. A new sequence's first job is never queued behind another sequence's later jobs. NF2 builds and proves it.
   - **Tiers (card-owner ruling (a), coordinator (3), 2026-10-03).** Class U sorts in three tiers, each by earliest `next_attempt_at`, then `rowid`; class A follows.
     - Tier 0: the first job (lowest `rowid` in the sequence) of each sequence with no accepted page.
     - Tier 1: a representative that is a later job, that is, an unpaged sequence's oldest-due job once its first job has run and while that job is not due again, so a sequence has one representative.
     - Tier 2: every other class-U job.
     - "Across sequences, by earliest due time" therefore holds within each tier, and a first job sorts ahead of every later job of any sequence.
   - **Condition (2), sizing.** Size k for the realistic first-pass set: one origin incident plus at most one per leg, with mutual exclusion credited (k ≈ 8-10). Keep (d) checked at that k in #651's binding.
   - **Condition (3).** NF-1's loud rule still applies to any due unaccepted job that is deferred (NF3, unchanged).
   - **Residual:** R6 (§9), verbatim.
   - **k_first = 1 + 4 × 1 = 5.**
     - Origin, 1. The first committed incident moves the owner into INTERVENTION (`book_account_owner.py:2093`). Any `_halt_db` caller can be it, for example `ordinary-unknown` (`:1906`), `barrier-expired` (`:1123`) or O3's `own-flat-deadline` (`:2009-2017`; register `:414`).
     - Legs, 4 × 1. `BOOK_LEGS` has four legs (`book_policy.py:179-197`). After the origin nothing is dispatched (register O1, `:411`; HR `:26`, `:164`), so further close outcomes come only from closes already sent, at most one per leg (register O9, `:420`). A close's outcome rows (O2b, O4's non-`Filled` terminal, O5-O8 and R-T8; register `:413`, `:415-419`; HR `:150-155`) are credited as mutually exclusive, so one per leg. All four legs have a close in flight together only in the scheduled flatten (`:1993-2003`).
   - **k floor = 8 (card-owner ruling (c), coordinator (3), 2026-10-03).** The ruling's formula gives k_first = 5, but the ruling states k ≈ 8-10. The floor is k_first plus margin, 8, the low end of the owner's range. It also covers a three-detector origin (HR `:115`: 3 + 4 = 7).
   - **Default k = 10**, twice k_first and inside the ruling's 8-10. The margin also covers some R-T9 findings (HR `:156`, `:174`) or per-fact rows (`:2116-2283`; `fact-time:` takes a fresh `uuid4()` per observation, `:2116`). Above k those are R6's later jobs; a representative is not deferred while at most k are due (NF2). 10 is also the smallest k that keeps the #628 suite (item 3).
   - **#651's binding** refuses k below the floor of 8 (its (e'), `fb3c3ba:124`) and checks (d) at the frozen k. At k = 10 and c = 2, (d) fails at #628's defaults, so OQ-CAP-3 chooses τ and W_j (§9).
   - **Withdrawn:** K_halt_max = 51, its default k of 64 (`4990ce7` §0.5 item 11) and #651's (e) k ≥ 51. The review of `4990ce7` found that count missed O3 (P2); that is moot, because O3 is an origin above. Its P3s on the `:2116` keying and the R-T owner list fell with the OWED paragraph they corrected: keying now affects only R6's later jobs.
12. **Halt-sequence key.** Chosen in this fold under coordinator (3)'s dispatch; coordinator (3) confirms at freeze.
   - **Rule.** In journal `rowid` order over every job, in every state, a job continues the previous job's sequence when the previous job's generation is at least 1 and its own is exactly one more. Otherwise it starts a sequence, whose id is its first job's `rowid`.
   - **Why generation runs.** `_halt_db` is the only writer of `incidents`. It stores the owner's current generation and then raises it by one (`book_account_owner.py:2091-2094`). Inside a halt, only a restart (`:445`) or a migration (`book_migration.py:412`) also raises it; the scheduled-exit raise needs NORMAL authority (`:1963-1969`), which INTERVENTION has revoked. Owner transactions are serialized, `read_incidents` returns rows in `rowid` order (`:815-816`), and `poll` inserts them in that order (`:405-420`). A halt's incidents are therefore consecutive generations in journal order.
   - **The other candidates.** Generation equality groups nothing, since no two incidents share a generation. `session_id` is not in an incident row (`_SCHEMA`, `:296-297`; `read_incidents`, `:812-815`), and adding it is an owner edit (§5). The halt record is the singleton `owner_state` row (`:718-720`), which the read-only seam does not read.
   - **One halt per owner DB today.** The only HALTED→RUNNING transition is the one-use bootstrap, which refuses once any incident row exists (`book_bootstrap.py:137-141`, `:174`; HR `:204`, "First release: no resume"). So two halts never share an owner DB, and the rule cannot merge them.
   - **Failure direction: over-split, which is safe.** A restart or migration inside a halt leaves a generation gap, so its later incidents start a new sequence. A malformed row (generation 0, `poll` `:409`) is a sequence of its own and ends the run, so inside a run it adds two sequences: itself and the remainder. Each split adds sequences, each with at most one representative, and removes none.
   - **Under-split (R7).** A replaced owner DB under the same journal (R4) whose first incident happens to continue the old run, or a future resume that does not raise generation before the next incident. **OWED** to the durable resume owner (TB-I3, HR `:203`): any HALTED→RUNNING transition raises generation, or this key is re-derived.
   - **Cost.** NF5 reads every job: at most n ≤ M (item 4).

A contradicted default, a missing producer or a necessary edit outside §5 returns NEEDS_CONTEXT.

## §1 — Goal, scope, prerequisites

**Goal.**
- #651 can declare `max_round_duration` from NF8 and refuse a notifier whose cap differs (`fb3c3ba:113`, `:136`), or a cap below the floor of 8 (§0.5 item 11).
- #637's notifier heartbeat can mark on NF6 (`828ddda:10`).
- #635's CLI can open the live journal without rebuilding it (NF7).
- Every other #628 behavior stays as merged (NF9).

**Scope.** Two config fields, `poll`'s known-keys set and over-bound event, `publish_due`'s selection, cap and `cap_deferred`, `progress()`, the `rebuild` keyword, and one new test file.

| ID | Item | State at draft | Blocks |
|---|---|---|---|
| P1 | #628 merged | **Done** (`6e679cc`) | Nothing |
| P2 | Coordinator (3) rules on D1, D2 and the empty-journal refusal (§0.5 items 4-6) and confirms the OQ-NF-1 record (item 7) | **Done** (2026-10-03) | Nothing |
| P3 | Sequencing with #635's D-MON-1 build (§5) | OPEN; recorded at dispatch | Dispatch |
| P4 | Coordinator (2) confirms coordinator (3)'s readings (i)-(iii) of the OQ-NF-3 ruling (§0.5 item 11) | OPEN; requested by coordinator (3) | Freeze |

## §2 — Measured-closure check

`book_incident_notifier.py` is in no measured closure. Checked at `04a86ac`:
- **S5 Stage 1c.** `stage1c_closure_table.py.txt . 04a86ac 04a86ac` lists 68 measured and 63 staging modules. The notifier is in neither list.
- **S5 records.** `git grep book_incident_notifier` over `docs/notes/2026-09-27-s5-part-a-measurement` and `docs/notes/2026-09-29-s5-c3-record` finds no match.
- **T00 P7 first-party closure** (40 modules, `2026-09-24-tradeify-t00-p7-closure.md:630`). The list is not in the repository. Static evidence instead: outside `docs/`, `git grep book_incident_notifier 04a86ac` matches only the module's own test and the path string in `scripts/check_durable_store_pragmas.py:54`. No module imports the notifier.

The worker re-runs the table from `origin/main` to `HEAD` (§7).

## §3 — Design: NF1-NF9 (names fixed by coordinator (3))

**NF1 — Cap.**
- Add `max_jobs_per_round: int = 10` to `NotifierConfig`, after `retry_max_s` (`:211`). 10 is above the floor of 8 (k_first = 5 plus margin) and is the smallest k that keeps the #628 suite (§0.5 items 3, 11).
- `__post_init__` runs before the digest. It refuses a `bool`, any non-`int` (including `2.0`) and any value below 1 with `NotifierConfigError("max_jobs_per_round must be a positive integer")`.
- `_CONFIG_KEYS` (`:74`) gains the key, so `from_mapping` passes it through (`:248`), and `resolved()` emits it.
- `publish_due` runs at most k job rounds per call.
- A nominated job uses its slot whether or not its round publishes. A job closed between the snapshot and its admission (J2, `:470-473`) is not replaced. Replacing it would break NF8's transaction count.

**NF2 — Priority** (owner readings OQ-NF-1 and OQ-NF-3, §0.5 items 7 and 11).
- **Class U** is `rounds = 0 OR channels_lost = 1` (§0.5 item 2). **Class A** is `rounds > 0 AND channels_lost = 0`: accepted, still pending, awaiting record-delivery (#635 `:134`).
- **Representatives.** Jobs fall into halt sequences (§0.5 item 12). A sequence *has an accepted page* when one of its jobs is class A or `delivered`. In each pass, a sequence with no accepted page and a due class-U job has one representative (ruling (a), §0.5 item 11). It is the sequence's first job (lowest `rowid`) when that job is due, which is tier 0; otherwise it is the due class-U job with the smallest (`next_attempt_at`, `rowid`), a later job, which is tier 1. Every other class-U job is tier 2. Such a sequence's first job is pending and class U, since a `delivered` or class-A job is an accepted page.
- **Order.** Class U by (tier; `next_attempt_at`; `rowid`), then class A by (`next_attempt_at`, `rowid`). Times compare as parsed instants (NF5). The first k are taken. The order is never newest-first, which can starve an older unaccepted incident while new ones keep arriving.
- **Condition (1) holds** (§0.5 item 11), whatever the clock, because tier 0 depends only on `rowid` and acceptance.
  - Within a sequence, its first job (0) or its representative (1) sorts ahead of its other class-U jobs (2).
  - Across sequences, order is by earliest due time, then `rowid`, within each tier.
  - A new sequence has no accepted page, so its due first job is tier 0. Tier 0 holds only first jobs, so every later job of another sequence (tier 1 or 2, or class A) sorts behind it (RC2(a), RC2(d)).
- **60 s guarantee (representatives; the ruling's two clauses under readings (i)-(iii), §0.5 item 11).** Suppose each pass has at most k due representatives and the clock does not step back. Then a sequence without an accepted page has an attempt in every pass in which it has a due class-U job: representatives fill the first slots, and a failed round leaves its job in class U, due again within `retry_max_s` (`:522-530`). Its attempts are therefore at most `retry_max_s` + L + poll_bound apart by the journal's clock (§0.5 item 1), until a page is accepted.
  - **Precondition:** `retry_max_s` + L + poll_bound < `ESCALATION_STEP_S` (60 s, `:60-62`). Then every 60 s escalation interval holds a retry for each such sequence. It is #651's binding check (d), at the frozen k (OQ-CAP-3, §9).
  - The premise counts sequences, not jobs: a sequence has at most one representative, and §0.5 item 12 makes one sequence per halt, plus one per owner restart or migration and up to two per malformed row (the row itself and, inside a run, the remainder it splits off). A pass with more than k due representatives is loud (NF3).
- **Representative spacing beyond the premise.**
  - A first job (tier 0) is attempted at most `retry_max_s` + (⌊A_0/k⌋ + 1)·L + poll_bound apart. A_0 is the number of due first jobs that precede it in (`next_attempt_at`, `rowid`) when it falls due. Only they can sort ahead of it, and each pass that defers it runs k of them.
  - That set only shrinks. A new job's due time is its poll time, never earlier; on a tie, its larger `rowid` sorts behind. A round that ends without raising either finds the job closed (J2 or J3, where `_transition` writes nothing) or sets `next_attempt_at` = now_P + delay > now_P (`:522-530`), so a job that ran never precedes it again.
  - A later-job representative (tier 1) sorts behind every due first job, and a failing first job is due again within `retry_max_s`. Beyond the premise its spacing has no bound, and every pass that defers it is loud (NF3).
- **Starvation-freedom (every class-U job X, clock not stepping back).** Let A be the number of due class-U jobs that precede X in (`next_attempt_at`, `rowid`) when X falls due; as above, that set only shrinks.
  - If at most u < k representatives are due in each pass while X waits, each pass that defers X runs at least k − u of those jobs. X runs within ⌊A/(k − u)⌋ + 1 passes, so its attempts are at most `retry_max_s` + (⌊A/(k − u)⌋ + 1)·L + poll_bound apart.
  - X's sequence having no accepted page does not lift the bound on u. While the sequence's first job is due, that job is the representative and X waits in tier 2; under reading (iii) the sequence's retry is that job's (§0.5 item 11).
  - Every pass that defers X is loud (NF3).
- **Normal case for every class-U job.** A pass with at most k due class-U jobs runs them all. With k at or above the floor of 8 (k_first = 5 plus margin), that covers a halt's realistic first-pass set (§0.5 item 11). A loud pass is not by itself a page (R6).
- **Class A has no bound.** A class-A job sorts behind every due class-U job, and a failing U job stays in class U each time it falls due again. While class-U load fills the cap, a due class-A job may never run. Each such pass defers only class A, so it is not loud (NF3) and `progress()` advances. The owner reading OQ-NF-1 permits this (§0.5 item 7).
  - Example (review of `7da0288`): k = 1, `retry_initial_s` = `retry_max_s` = 2 s, passes 1 s apart, two class-U jobs that always fail and one due class-A job. Over 40 passes the class-A job ran 0 times, and 39 passes were not loud.
  - With no class-U load, class A rotates like class U (RC3(b)).
- **A backward clock loosens these bounds.** The caller supplies the clock; `_now` checks only that it is timezone-aware (`:363-367`), and #651 anticipates a backward step (`fb3c3ba:78`). A step back of B does two things:
  - A waiting job is not due until the clock again reaches its due time, which adds up to B.
  - An incident polled meanwhile can get an earlier due time. N such incidents then count in A_0 or A.
  - Rotation still holds, because a re-run job and the waiting job are compared at the same now_P. Tier 0, and so condition (1), does not depend on the clock.
- **Wall-clock note.** Every event in a pass carries that pass's `now`. A job's publish can start up to `max_round_duration` after it, so publish starts can be that much further apart than the journal shows. Routed with OQ-CAP-3 (§9).

**NF3 — Loud deferral** (owner condition (1)).
- When the snapshot defers at least one due job, the pass writes one evidence event, `cap_deferred`. Its `incident_key` and `channel` are NULL, `at` is the pass's `now`, and its detail is `{unaccepted, accepted}`: counts of deferred due jobs per class, nothing else.
- The event is written in the snapshot transaction, so NF8's transaction count does not change.
- `publish_due` returns True when it deferred a due class-U job, and False otherwise.
- On True, `run_once` does not refresh `liveness()` and does not increment `progress()`, even though it completed. #637's notifier heartbeat stops marking, and the dead-man check pages once no mark has arrived for T_n (HR `:71`, condition 4). A loud run shorter than T_n pages nobody (R6).
- A pass that defers only class-A jobs still writes `cap_deferred`, but `liveness()` and `progress()` advance (NF2: class A has no bound).
- **Post-rebuild backlog.** After a rebuild or first start, every retained incident becomes a `rounds = 0` job with the same due time (#628 card `:86-90`), and no sequence has an accepted page. A new incident in an existing sequence waits behind them for up to ⌊A/k⌋ passes, and each of those passes is loud. For example, with 120 re-owed jobs in one sequence, k = 10, and a new incident in that sequence arriving before pass 2, the new incident's first attempt is in pass 13; passes 1-12 are loud. A new incident that starts a sequence is tier 0, so it runs ahead of every re-owed later job: first in pass 2 in RC4(b).

**NF4 — Ingestion bound.**
- **Known keys.** A per-instance set is loaded once in the constructor's transaction, after the schema statements, with `SELECT incident_key FROM jobs` (every state). `poll` INSERTs only keys not in the set, still with `INSERT OR IGNORE`, so J1 is unchanged. `poll` opens its one transaction on every call, even when every key is known (as at `:411`); NF8 counts it.
- The set is updated only after `poll`'s transaction commits, with the keys it inserted or found already present. A key added before `COMMIT` would be lost if the commit failed.
- Reading and parsing all n rows stays O(n). An owner-side incremental read is OQ-NF-2, out of scope (an owner packet).
- **Bound.** New field `max_retained_incidents: int = 1000`, validated like NF1, with the same exposure.
- When n (rows read this poll, malformed ones included) crosses from at-or-below M to above it, `poll` writes one evidence event, `retained_incidents_over_bound` `{count: n}`, in its transaction. The crossing state is per instance, starts at-or-below, and changes only after the commit.
- Processing continues, and nothing is dropped. NF8's bound assumes n ≤ M.
- **Residual R2.** The set assumes that only this instance fills and initializes the journal. Two paths would make it skip owed keys that #628 would have re-inserted:
  - a second `rebuild=True` instance moves the journal aside, or initializes a missing or emptied one;
  - the journal is removed under this instance, its next open re-creates the file with no tables (`:303-304`), and another open initializes it.
  - NF7 closes the second path for #635's CLI: a `rebuild=False` open refuses a missing, empty, table-less or foreign-schema journal and initializes nothing (§0.5 item 6), so this instance keeps raising, which is loud (RC8(f)). The first path remains: J0 serializes rounds per notifier only (#628 card `:126`), and two notifier instances on one journal stay out of scope.

**NF5 — Pending fetch.**
- In the snapshot transaction, `publish_due` reads `rowid`, `incident_key`, `generation`, `state`, `reason`, `detected_at`, `next_attempt_at`, `rounds` and `channels_lost` for every job, in every state (D1, RULED: no `LIMIT`; at most n ≤ M jobs, §0.5 item 4). Sequences and accepted pages come from all of them (§0.5 item 12).
- "Due" is unchanged: `datetime.fromisoformat(next_attempt_at) <= now`, as at `:459`.
- The due pending jobs are sorted by NF2's key, and the first k are taken.
- Timestamps are never compared as SQL strings. ISO strings with different UTC offsets do not sort as instants, and a local-time clock produces both across a DST change.

**NF6 — Rollback-safe progress.**
- New `progress()` returns a per-instance int that starts at 0 and never decreases. It counts the `run_once` calls that completed without raising and without a loud pass.
- It is incremented exactly where `_last_loop_at` is set (`:436`), and a loud pass skips both together. `publish_due` and `poll` called alone change neither.
- `liveness()` keeps its contract apart from the NF3 skip, and its docstring says so.
- A heartbeat wrapper marks on an increase in `progress()`, never on a clock value (#651 `fb3c3ba:72`; #637 `828ddda:10`). A backward clock can move `liveness()` back; `progress()` never goes back.

**NF7 — No-rebuild open.**
- `IncidentNotifier.__init__` gains the keyword-only `rebuild=True`. True keeps today's behavior.
- With `rebuild=False`, a missing journal raises `NotifierStoreError` and creates no file or directory.
- With `rebuild=False`, a `_journal_fault` fault raises `NotifierStoreError`, with no `_move_aside` and no `journal_rebuilt` event.
- Every connection of a `rebuild=False` instance opens with `mode=rw` and skips the `mkdir` (D2, RULED). A journal removed after construction then fails instead of being created.
- With `rebuild=False`, any schema other than `_JOURNAL_SCHEMA` is refused, including an empty or table-less file (§0.5 item 6, RULED). The constructor's transaction reads `_journal_schema(db)` before any schema statement and raises `NotifierStoreError` unless it equals `_JOURNAL_SCHEMA`; nothing is initialized. The check sits in that transaction, so a journal emptied or replaced after `_journal_fault` is refused too. `_journal_fault`'s `{}` acceptance (`:341`) is unchanged and still serves `rebuild=True`.
- A hot rollback journal is rolled back by the writable open, as at `:333`, and nothing is moved.
- #635's CLI constructs with `rebuild=False` (`f4d1589:145`), which closes its pre-check-versus-constructor race (`:141`).

**NF8 — Whole-invocation bound.**

`run_once <= W_o + T_parse(n <= M) + (2 + 2·k·c)·W_j + k·c·τ + ε`

- W_o is the owner read's busy wait: 5 s (`book_account_owner.py:811-812`).
- T_parse(n) is the CPU time to read and parse n rows, then fetch at most n jobs, group them (§0.5 item 12), and filter and sort the pending ones.
- **2 + 2·k·c journal transactions** run on the pass thread: the poll (opened on every call, NF4), the snapshot (which holds `cap_deferred`), and one admission (`:470`) plus one close (`:486`) per (job, channel). A refused channel skips its close, and a closed job ends its round early; both only lower the count.
- W_j is each transaction's lock wait. `BEGIN IMMEDIATE` waits up to 5 s (`:304`). In the default rollback journal, `COMMIT` can wait another 5 s behind a reader, such as #635's read-only checks (`f4d1589:141`, `:146`), so W_j can reach 10 s.
- A run makes at most k·c bounded publishes, each waiting at most τ (`join`, `:575`).
- ε is fsync and other CPU time, which no declared bound covers. HH7 measures it (`fb3c3ba:203`).
- Late-outcome threads contend for the same lock; that wait is inside W_j.
- **At #628's defaults** (τ = 10 s, c = 2) and k = 1, the bound is 5 + 6·5 + 20 = 55 s, or 85 s with W_j = 10 s, before T_parse. On the notifier side, #651's condition (b) needs `max_round_duration` below 30 s at the lean T_n = 60 s (`fb3c3ba:119-122`, `:259`). So OQ-CAP-3 goes to #651's freeze: choose τ, the declared W_j, `retry_max_s` or T_n. k is floored at 8 (k_first = 5 plus margin) and defaults to 10 (§0.5 item 11).

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
- `rebuild=False` never creates, initializes or moves aside a journal;
- one `run_once` stays within NF8's counts;
- and NF9 holds.

**Falsifier.** Any one of these refutes H:
- a pass that runs more than k jobs, or that refills the slot of a closed nominated job;
- a class-A job running before a due class-U job, or class U out of NF2's (tier, due time, `rowid`) order, or sequences and accepted pages that differ from §0.5 item 12;
- a new sequence's due first job deferred in a pass that runs a later job of another sequence (condition (1));
- under persistent failure and a clock that does not step back, a representative, or a class-U job within NF2's premise, that does not run within NF2's bounds (class A has none);
- a pass that defers a due class-U job yet refreshes `liveness()` or advances `progress()`;
- a class-A-only deferral that stops `liveness()` or `progress()`;
- more than one `cap_deferred` in a pass, or counts that differ from the deferred jobs;
- an INSERT for a known key, or a key lost after a failed `poll` commit;
- `retained_incidents_over_bound` written other than once per crossing, or a crossing lost after a failed `poll` commit;
- a pending job above M that is never attempted;
- `progress()` decreasing, or changing on a `run_once` that raises or is loud;
- `rebuild=False` creating a file, directory or table, accepting a journal whose schema is not `_JOURNAL_SCHEMA`, moving a journal aside or writing `journal_rebuilt`;
- a `run_once` with more than 2 + 2·k·c journal transactions, more than k·c publishes, or more than one owner read;
- any #628 test failing, or a change to an NF9 item;
- a configuration that accepts 0, a negative value, a `bool` or a non-`int` for either new field, or that fails the `resolved()`/`from_mapping` round trip.

## §5 — Files

**Allowed:**
- `ops/c1_rail/book_incident_notifier.py`, **only** these parts:
  - `_CONFIG_KEYS` (`:74`);
  - the two `NotifierConfig` fields, their validation and their `resolved()` entries (`:205-256`);
  - `__init__` (`:266-291`): the `rebuild` keyword, the `rebuild=False` schema refusal (NF7), the known-keys load, and the progress and crossing state;
  - the connect lines of `_journal` (`:302-304`) and `_journal_fault` (`:332`), through one new private helper (D2, RULED by coordinator (3));
  - `poll` (`:396-421`): the known-keys filter and the over-bound event;
  - `run_once` (`:425-436`), the `liveness` docstring (`:438-445`), and a new `progress()` beside them;
  - `publish_due` and its docstring (`:447-461`), with any new private helper it calls for NF2's sequences (§0.5 item 12);
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
- RC2, RC3, RC5 and RC9 may seed job state with direct `UPDATE`s of `state`, `rounds`, `channels_lost` and `next_attempt_at` in the test's own journal.
- **Run the file at base first and record the failures.** The fields and the keyword are absent at base. RC10 asserts the field's name in the error message, so `from_mapping`'s base refusal ("unknown notifier config keys") does not satisfy it.

| ID | Test | Basis |
|---|---|---|
| RC1 | `test_cap_admits_exactly_k`. (a) Five never-attempted due jobs, k = 2, a delivering channel: the passes attempt [1,2], then [3,4], then [5]. (b) k = 2 and three due jobs, where the channel's publish of job 1 calls `record_delivery` for job 2. Job 2 gets no `attempt` (J2), and job 3 is not attempted in that pass. That pass's `cap_deferred` is `{unaccepted: 1, accepted: 0}` | NF1 |
| RC2 | `test_nf2_order_representatives_then_class_u_then_class_a`. (a) One pass, k = 8, a delivering channel. Ten rows with generations 1, 2 \| 10, 11, 12 \| 20, 21 \| 30, 31 \| 40 form sequences SB, SA, SC, SD and SE (§0.5 item 12), with seeded job state. SB: class A at t−55, `channels_lost = 1` at t−12. SA: `channels_lost = 1` at t+8 (its first job, not due), `channels_lost = 1` at t−22, `rounds = 0` at t−32. SC: `channels_lost = 1` at t−2 (its first job, due), `rounds = 0` at t−12. SD: `delivered`, `rounds = 0` at t−12. SE: `rounds = 0` at t−12. Expected attempt order: tier 0, SE t−12 then SC t−2 (due order, the reverse of `rowid` order); tier 1, SA t−32, SA's representative, a later job behind SE's first job although due earlier; tier 2 by (due, `rowid`): SA t−22, SB t−12, SC t−12, SD t−12; then class A t−55. SB and SD have accepted pages, so they have no representative. The clock never steps back: this is the state the tiered order reaches from polls at t−60 (SB), t−50 (SA's first two), t−32 (SA's third, SC's first) and t−12 (the rest), with passes at those times and t−40 under caps 2, 2, 2, 3 and 3, `retry_initial_s` = 5 s, `retry_max_s` = 30 s, and every round lost except SB's first (accepted at t−60) and SD's first (delivered at t−12). (b) One poll of rows with generations 5, 6, 8, a malformed row (generation 0) and 1, k = 5: the sequences are {5, 6}, {8}, {malformed} and {1}, and the order is 5, 8, malformed, 1 (tier 0), then 6. (c) Two first jobs (tier 0) whose `next_attempt_at` strings carry different UTC offsets and sort the other way as text: the earlier instant runs first. (d) k = 1, a channel that always rejects. S1 (generations 1, 2): `channels_lost = 1` at t+10, `rounds = 0` at t−10, the state after the pass at t−10 ran S1's first job and deferred the later job polled with it. S2 (generation 5), a new sequence: `rounds = 0` at t. The pass attempts only S2's first job; S1's representative, a later job due earlier, is deferred, with one `cap_deferred` `{unaccepted: 1, accepted: 0}`, and the pass is loud | NF2, NF5 |
| RC3 | `test_rotation_within_a_class_under_persistent_failure`. (a) Class U: five jobs, k = 2, a channel that always rejects, and the clock advanced 60 s (more than `retry_max_s`) before each pass. The attempted sets are {1,2}, {1,3}, {1,4}, {1,5}, {1,2}: job 1, the sequence's first job, runs in every pass (tier 0), and each of jobs 2-5 runs in any four consecutive passes. (b) Class A: three jobs, k = 1, a channel that accepts without delivery, and the same clock. Passes 4-9 run jobs 1, 2, 3, 1, 2, 3. (a) and (b) use consecutive generations (one sequence). (c) Two sequences: S1, generations 1-7, with generation 1 seeded class A and 2-7 class U due at t−60, t−50, …, t−10; S2, generations 20-21, class U due at t−5. k = 2, a channel that always rejects, and the clock advanced 60 s before each pass. In each of 12 passes S2's first job runs (tier 0), and the other slot rotates in (due, `rowid`) order through S1's six class-U jobs and S2's generation 21 (tier 2), so each of those seven runs in any 7 consecutive passes. S1's class-A job never runs | NF2 |
| RC4 | `test_post_rebuild_backlog_is_loud_and_representatives_first`. A journal of unreadable bytes and `rebuild=True` (`journal_rebuilt` written). `read_incidents` returns 120 rows with generations 1-120 (one sequence), k = 10, a delivering channel, and the clock advances 1 s per pass. Pass 1 attempts the 10 lowest `rowid`s and writes `cap_deferred` `{110, 0}`; afterwards `progress() == 0` and `liveness() is None`. (a) A 121st row with generation 121 (the same sequence, which now has accepted pages) is committed before pass 2. Its first attempt is in pass 13, after every re-owed job. Passes 1-12 are each loud, with one `cap_deferred` each (`unaccepted` 110, 101, 91, …, 1). Pass 13 is not loud: `progress() == 1`, and `liveness()` equals pass 13's clock. (b) The same, but the 121st row has generation 200, a new sequence as after an owner restart. It is the first job attempted in pass 2, ahead of 110 older re-owed jobs, and the loudness and `cap_deferred` counts are as in (a). The test asserts state and order, not elapsed time | NF2, NF3 |
| RC5 | `test_cap_deferred_once_per_pass_with_counts_and_loudness`. (a) Seeded due jobs, 3 in class U and 2 in class A, k = 2: exactly one `cap_deferred`, `{unaccepted: 1, accepted: 2}`, with exactly those two detail keys. The `run_once` is loud: `progress()` and `liveness()` are unchanged. (b) Only 3 due class-A jobs, k = 2: `{unaccepted: 0, accepted: 1}`, and the pass is not loud (`progress()` + 1, `liveness()` = the clock). (c) A pass with at most k due jobs writes no `cap_deferred` | NF3 |
| RC6 | `test_known_keys_and_retained_bound`. Statements are traced by a wrapper around `_journal` that calls `set_trace_callback` on the yielded connection. (a) A second `poll` over the same rows executes no INSERT into `jobs`; a new row adds exactly one; a fresh instance on the same journal inserts none. (b) A `poll` whose transaction fails (a patched `_event` raises `sqlite3.OperationalError` on `detected`) raises `NotifierStoreError`, and the next `poll` inserts that key. (c) With M = 3, polls over 2, 4, 5, 3 and 4 rows write `retained_incidents_over_bound` exactly twice, `{count: 4}` each time, and every row has a job. (d) With M = 3, k = 5 and five due pending jobs, all five are attempted in one pass. (e) With M = 3, a `poll` over 4 new rows whose `COMMIT` fails (for example, a second connection holds a read transaction on the journal past the 5 s busy wait) raises `NotifierStoreError` and leaves no job and no event. After the reader ends, the next `poll` over the same rows inserts all 4 keys and writes `retained_incidents_over_bound` `{count: 4}` exactly once | NF4, NF5 (D1) |
| RC7 | `test_progress_counts_clean_non_loud_loops_only`. `progress()` is 0 at construction and rises by 1 per clean `run_once`. It does not change on a `run_once` that raises (a raising `read_incidents`; a journal replaced by a directory, as T17 does) or on a loud pass. With the clock stepped back 1 h between clean loops, `liveness()` moves back while `progress()` still rises by 1 | NF6 |
| RC8 | `test_rebuild_false_refuses_missing_faulty_and_uninitialized_journals`. (a) A missing path inside a missing directory: `NotifierStoreError`, and the listing of `tmp_path` is unchanged. (b) The race: `Path.is_file` patched to report True for a missing path still raises and creates nothing. (c) Unreadable bytes, a failed integrity check and a foreign schema: each raises; the file bytes, any sidecars and the listing are unchanged; no `*.corrupt-*` file and no `journal_rebuilt`. (d) A valid journal constructs, and `record_delivery` closes a job. With `rebuild=True`, the faulty files of (c) are still moved aside. (e) A 0-byte file and a table-less SQLite file: each raises `NotifierStoreError`; no table is created, nothing is moved aside and no `journal_rebuilt` is written. With `rebuild=True`, both are still initialized as fresh journals (`:324`). (f) The table-less file re-created under a running notifier: a `rebuild=True` instance N has three pending jobs, and the test renames the journal away. N's next `run_once` raises and leaves a file with no tables at the path. A `rebuild=False` construction there raises and creates no table. N's next `run_once` still raises, and N's `progress()` has not advanced since the rename | NF7, NF4 (R2) |
| RC9 | `test_run_once_stays_within_nf8_counts`. `read_incidents` returns M = 50 rows, all already journaled: 45 seeded delivered and 5 due pending. k = 2, and c = 2 channels that both reject at once. On the pass thread: `read_incidents` is called once; INSERTs into `jobs` = 0; `_journal` is entered exactly 2 + 2·k·c = 10 times, with `cap_deferred` inside the snapshot transaction; `_bounded_publish` is called exactly k·c = 4 times. This setup attains NF8's counts, so "exactly" is the bound: `poll` opens its transaction with nothing to insert (NF4), neither channel is refused, and no nominated job closes early. The parse time for M rows is printed for the return, not asserted | NF8 |
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
| Representatives ignored: class U by (due, `rowid`) only | RC2(a), RC2(d), RC3(a), RC3(c), RC4(b) |
| A first job not ahead of a later-job representative (one representative tier by due, this card's previous order) | RC2(a), RC2(d), RC3(a), RC3(c) |
| Representatives across sequences ordered by `rowid`, not due time | RC2(a) |
| Every job its own sequence (generation equality) | RC2(a), RC2(b), RC3(c) |
| One sequence per journal (no generation-gap split) | RC2(a), RC2(b), RC4(b) |
| A malformed row (generation 0) joins a run | RC2(b) |
| A later-job representative by lowest `rowid`, not earliest due | RC2(a) |
| A sequence with an accepted page keeps a representative | RC2(a) |
| Sequences or accepted pages from pending jobs only, or `delivered` not counted | RC2(a) |
| A loud pass refreshes `liveness()` or `progress()` | RC4, RC5, RC7 |
| A class-A-only deferral is loud | RC5(b) |
| `cap_deferred` in its own transaction | RC9 |
| Known keys ignored | RC6(a), RC9 |
| Known set updated before `COMMIT` | RC6(b), RC6(e) |
| Crossing state updated before `COMMIT` | RC6(e) |
| `poll` opens no transaction when every key is known | RC9 |
| `retained_incidents_over_bound` on every poll above M | RC6(c) |
| `LIMIT M` on the pending fetch | RC6(d) |
| `progress()` derived from the clock | RC7 |
| `rebuild` ignored; an `is_file` check without `mode=rw` | RC8(a)-(c); RC8(b) |
| An empty or table-less journal initialized under `rebuild=False` | RC8(e), RC8(f) |
| An `incident_key` tiebreak | The #628 regression |

**Return taxonomy.**
- **DONE:** every RC test recorded red at base and green at head; every mutant red; the regression, `test-ops`, `check` and the full suite green, with records cited; the diff inside §5.
- **DONE_WITH_CONCERNS:** the selected outcome holds, with a disclosed baseline limitation unrelated to this patch that reproduces on unmodified origin/main.
- **NEEDS_CONTEXT:** a missing input, a contradicted default, or a #635 landing that overlaps §5's parts.
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

**Full suite.** Joshua confirmed on 2026-10-03 at 18:22Z, directly to coordinator (3) ("sounds good"), that a code PR needing coordinator (3)'s acceptance waits for the full suite. **Confirmed by coordinator (3)** (AUTH: coordinator (3)'s 2026-10-03 fold dispatch).

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
- **D1, RULED** by coordinator (3), card owner, 2026-10-03: NF5 reads every pending job with no SQL `LIMIT` (§0.5 item 4).
- **D2, RULED** by coordinator (3), 2026-10-03: `mode=rw` and no `mkdir` under `rebuild=False`; §5 widened (§0.5 item 5).
- **Empty-journal refusal, RULED** by coordinator (3), 2026-10-03: `rebuild=False` refuses any schema other than `_JOURNAL_SCHEMA` (§0.5 item 6).
- **OQ-NF-1:** owner reading, RULED; the record is confirmed by coordinator (3) (§0.5 item 7).
- **OQ-NF-3, RULED (a), the first-page reading,** by coordinator (2), halt/resume owner, 2026-10-03: tiered representatives first (NF2), k_first = 5, a k floor of 8, default k = 10, and (d) checked at that k by #651's binding (§0.5 item 11). It supersedes the earlier sizing condition (K_halt_max = 51, default 64).
- **Card-owner rulings (a)-(c),** coordinator (3), 2026-10-03: (a) tiers inside class U (NF2); (b) readings (i)-(iii) of OQ-NF-3, PENDING coordinator (2)'s confirmation (P4); (c) the k floor of 8 (§0.5 item 11).
- **Halt-sequence key:** generation runs (§0.5 item 12), chosen in this fold; coordinator (3) confirms at freeze.
- **Full-suite rule:** confirmed by coordinator (3) (§7).

**Residuals.**
- **R1. A deterministic raise in a round.** An example is `assert_no_secrets` rejecting a job's reason (`:464`; `c1_rail_telemetry.py:127-144`).
  - The job stays at `rounds = 0` with its due time unchanged, so it remains the earliest-due class-U job. It heads every pass and blocks every job behind it. Under `rowid` order it blocked only later rows.
  - It is loud: `run_once` raises, so `liveness()` and `progress()` stop.
  - It is latent: owner reasons are codes or canonical JSON.
- **R2. Known keys versus a second instance** (NF4).
- **R3. A backward clock** loosens NF2's bounds (NF2).
- **R4. pending ≤ n.** D1's bound assumes one owner DB feeds the journal and never deletes incidents. Replacing the owner DB under an existing journal breaks it, and can continue a generation run across the replacement (R7).
- **R5. Wall-clock spacing** can exceed the journal's spacing by up to `max_round_duration` (NF2).
- **R6. A loud pass is not a page** (NF3). The heartbeat resumes marking on the next clean pass, so a class-U backlog that clears in less than T_n pages nobody, although a later job's retry gap exceeds 60 s.
  - Example: L = 5 s, `retry_max_s` = 30 s, k = 10 and 60 due class-U jobs ahead of a later job X of a sequence with an accepted page, ignoring poll_bound. Six loud passes (30 s, under T_n = 60 s) put X's attempts 30 + 7·5 = 65 s apart, and only `cap_deferred` rows record it. A representative is not deferred while at most k are due (NF2).
  - Accepted residual, verbatim (OQ-NF-3, §0.5 item 11): "beyond the halt's first page (and any sequence without an accepted page), a burst above k can stretch a later unaccepted job's retry gap past 60 s without a page; recorded in cap_deferred; accepted by the halt/resume owner, 2026-10-03."
  - **Scope under reading (iii)** (coordinator (3)'s, PENDING coordinator (2)'s confirmation; §0.5 item 11). The guarantee is one representative retry per unpaged sequence in each 60 s window. In a burst above k, an unpaged sequence's non-representative jobs, including its later jobs while its first job is due (NF2), are the residual's "(and any sequence without an accepted page)".
- **R7. Halt-sequence key** (§0.5 item 12). It over-splits at each owner restart or migration, which adds a sequence, and at each malformed row, which adds up to two (the row and, inside a run, the remainder). Each added sequence has at most one representative (safe). It under-splits only across a replaced owner DB (R4) or under a future resume that does not raise generation, which is **OWED** to the durable resume owner (TB-I3, HR `:203`).

**OPEN.**
- **OQ-NF-2** (the `book_account_owner.py` owner). An incremental `read_incidents`. Out of scope.
- **OQ-CAP-3** (coordinator (3), for #651's freeze).
  - Choose τ, W_j, `retry_max_s` or T_n so that NF8 stays below 30 s, and account for R5. k is floored at 8 (k_first = 5 plus margin) and defaults to 10 (§0.5 item 11). With W_j at the code's 5 s, the default `retry_max_s` of 30 s cannot pass the check below: L ≥ NF8 and poll_bound ≥ W_o + W_j = 10 s, so the check needs `retry_max_s` + 2·poll_bound + (1 + 2kc)·W_j + kcτ < 60 s, and 30 + 20 + 15 > 60 at k = c = 1 (review of `5d2356c`, P3-F). It passes only with a declared W_j well below 5 s, as in the feasible point below.
  - **BINDING CHECK (extension, routed to #651).** #651's binding validator (`validate_binding`, `fb3c3ba:137`) refuses a binding unless `retry_max_s` + `max_notifier_loop_interval` + poll_bound < `ESCALATION_STEP_S`: #651's constraint (d) (`fb3c3ba:123`). This is NF2's class-U precondition. The binding's `retry_max_s` must equal the notifier's configured value (`fb3c3ba:136`). #651's import rule bans `book_incident_notifier` (`fb3c3ba:151`), so `book_host` restates `ESCALATION_STEP_S` (`:60-62`) as 60.0, and HH4 pins it to this module's constant (`fb3c3ba:138`, `:200`). #651's (b) does not imply (d): NF8 = 10 s and L = 35 s can pass (b), but 30 + 35 > 60 s.
  - **(d) at the default k = 10, c = 2.** Since L ≥ NF8, (d) needs `retry_max_s` + 2·W_o + 2·T_parse + (3 + 2kc)·W_j + kcτ < 60 s, before ε and slack. With W_o = 5 s, that is `retry_max_s` + 2·T_parse + 43·W_j + 20·τ < 50 s.
    - #628's defaults fail: 30 + 43·5 + 20·10 = 445 s. W_j = 5 s alone gives 215 s, so no τ passes. Each term alone needs τ < 2.5 s and W_j < 50/43 ≈ 1.16 s. OQ-CAP-3 must choose τ and the declared W_j.
    - Feasible: τ = 0.5 s, W_j = 0.1 s and T_parse = 0.25 s at the default `retry_max_s` of 30 s give 30 + 0.5 + 4.3 + 10 = 44.8 s, leaving 5.2 s for ε and slack. NF8 is then 5 + 0.25 + 4.2 + 10 = 19.45 s, under (b)'s 30 s at T_n = 60 s. τ = 1 s also passes (d) with `retry_max_s` = 20 s (44.8 s), but NF8 = 29.45 s then needs T_n above 73.9 s, about 75 s, for (b), with L = NF8, P_n = 10 s and `ping_timeout` = 5 s (10 + 29.45 + 29.45 + 5).
    - **W_j = 0.1 s is a declared operating assumption, not a code bound.** The code lets each transaction wait 5 s for the lock (`:304`), or 10 s with a `COMMIT` wait (NF8), and HH7 measures without contention. Every competing journal holder (late-outcome threads, #635's CLI and its read-only checks) must release the lock within the declared W_j. OQ-CAP-3 must establish that, as it must establish that the provider answers within τ.
  - Once this card lands, #651 §0.5 item 6 (`fb3c3ba:79`, "Merged #628 has no job cap") is stale.

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
  - OQ-NF-3's state, coordinator (2)'s confirmation of readings (i)-(iii) (P4) and the halt-sequence key's confirmation (§9);
  - the #635 sequencing;
  - every moved anchor.
- **Executor (planned):** one Claude Code (Opus) worker session, seat worker, in a worktree under `.claude/worktrees/`. It works on a pushed `claude/*` branch, with no PR unless the coordinator records one.
- **Pre-dispatch checks:** the first two §10 hooks, run on the frozen file.
