# Dot card 01: November 2026 calendar ratification follow-through

**Type:** cc_handoff (dot release card; the first released assignment under the dot charter), revision 4 (successor routing amendment; see below).

**Status:** REVISION 4, pending its release comment (successor routing; see below). *Revision 3 status, superseded:* RELEASE-READY (frozen, revision 3) — HELD until the B3 focused re-review of revision 3 is CLEAN. #622 has merged (B15). Released by a `[coordinator (3) → hyper]` comment on #622 after that verdict; not released until then.
- Revision 1 (`3c1655fc9dff02b9edabd774e806a46cc39563ca`) was never released. Revision 2 replaces it before release. It folds the refute review of revision 1 (0 P1, 5 P2, 5 P3) and the binding structure coordinator (3) and Coordinator 2 accepted on 2026-10-03, which replaces revision 1's "the dot is the executor".
- Revision 2 (`524fcd12350b67528818c23751a9581098949d6e`) was never released: the B3 executive review was NOT CLEAN (2 P2, 1 P3). Revision 3 folds it and binds B15 (#622 merged).
- Committed before any execution under the committed-handoff rule. The release record is a `[coordinator (3) → hyper]` comment on #622, posted by coordinator (3) after the B3 re-review is CLEAN. It cites this card's revision-3 commit SHA (40 characters), the §0.1 B-row values and the executive-review verdict (B3). This file is not edited to record the release. After release, a change to any frozen section is a new card.

**Revision 4 — successor routing amendment (coordinator (4), card owner by succession from coordinator (3); 2026-10-05).** This governs over revision 3 where they differ. It is not released until C5 posts the release record (below).
- **Why:** the bound executor, Navigator `01a0ff7c-9b6e-70f7-96a8-8ea3f8a4b0d0`, returned Phase-0 `NEEDS_CONTEXT` on its local surface: Git "dubious ownership", an inaccessible local `gh` configuration, and an unverified operations environment and real hooks. It made no edits. C5 verified that this executor was the historically bound one; its old chat title does not invalidate the binding.
- **Successor executor:** the Codex deployment coordinator **C5** (`01a107d7-4608-7562-83e8-bbd58e14fe38`), executing **locally** on a working, validated operations environment (`fp.py doctor` passing, real hooks installed). It acts in the **executor role under this card's unchanged `worker` authority block**: the same capabilities and constraints, with no ratify, merge or main write. C5's coordinator role (relay and combined acceptance) does not widen this grant.
- **Retirement:** Navigator's execution role is **retired when, and only when, C5 posts the revision-4 release record**. No duplicate worker and no new session.
- **Unchanged:**
  - B9's exact three-file footprint and branch;
  - §2's exact edits;
  - B13's real hook proof, made in a fresh disposable worktree before any push;
  - red/green launcher records;
  - the independent review (B3 lane; the reviewer is not C5);
  - the required checks;
  - merge authority, which stays separate: the merge-order agent merges on Joshua's standing go;
  - §5's forbidden list, with "hyper" read as "the dispatching coordinator";
  - no calendar-byte or evidence-byte change.
- **B14 is BOUND** (from Joshua's own message, verified by C5 through `read_thread` of hyper's durable thread; not a paraphrase):
  - Hyper's candidate request (turn `01a1089e-fe31-742d-a30d-9eb12dcdf075`) names digest `b89562a58a665daa4054f310f41007f815bb45b54444c6404ad463ac0b60aad7`.
  - Joshua's next substantive reply (turn `01a108a1-99df-73b9-a54a-41f14ae79cfc`) supplies the values:
    - `NOV_RATIFIED_UTC` = `2026-10-04T20:36:11Z`;
    - `NOV_INSTRUCTION` = his full original wording, verbatim: "ratify the calendar. i have opened grafana in the in chat browser, complete as many of the steps you mentioned as you can, ping me when you need me".
  - This is contextual binding of his existing act, not a new ratification and not an invented phrase. The executor binds the candidate's identity (digest, card revision, release comment 5965599860 on #622) before writing the row.
- **B14 phrase rule, explicitly overridden for this act** (revision 3 `:125` "Reply: ratify calendar b89562a5", and `:287`'s stop if the reply "does not ratify digest"). Revision 4 accepts Joshua's 20:36:11Z reply as B14 by contextual binding: hyper's immediately preceding request named digest `b89562a5…`, and his reply ("ratify the calendar") is the next substantive response to it. C5 verified both turns directly, and C5 and coordinator (4) accept the reading. Under this override, `:125` and `:287` are satisfied for this act.
- **B14 provenance:** the revision-4 B14 row above replaces "values arrive by hyper's dispatch". The authority-block constraint `b14_values_only_from_hyper_dispatch` is read as "only from the B14 values bound in this card" (the block itself is unchanged).
- **Substitution table.** Every revision-3 line that names an old party reads as follows (for example B3, B11, §3 flow, §5, §7 and §8):

  | Revision 3 | Revision 4 |
  |---|---|
  | hyper (as dispatcher, notifier, relay or acknowledger) | C5's relay; card questions go to coordinator (4) |
  | worker `01a0ff7c-9b6e-70f7-96a8-8ea3f8a4b0d0` (including §5 "dispatching any worker other than …") | C5 as the local executor; no other executor is dispatched |
  | coordinator (3), Coordinator 2 | coordinator (4) |
  | "release record", "revision-3 SHA" (PR body and §3 steps) | the revision-4 release comment and the revision-4 SHA |

- **Recipients:** returns go to C5's relay. Card questions go to coordinator (4). Retired coordinators (2) and (3) are not recipients.
- **Release record:** a `[coordinator (4) → C5]` comment on #622 citing this revision's 40-character SHA, posted after an independent focused review of this amendment is CLEAN.

**Who does what.**

| Role | Holder | Seat, grants and limits |
|---|---|---|
| Dispatching coordinator | **hyper**: OpenAI dot, conversation `01a0ff79-c8a3-77b4-b0eb-83b11cce90f4`, durable host | `coordinator` seat (`scripts/seat_authority.yml:96-100`), narrowed by this card to `repository.read` (`:37`, low) and `handoff.dispatch` (`:46`, medium), the latter for the one worker named below only. Hyper does not execute: no worktree write, test run, push or PR. |
| Executor | Worker "Check First Passage readiness", `01a0ff7c-9b6e-70f7-96a8-8ea3f8a4b0d0`, explicitly rebound to this card | `worker` seat (`:105-108`) with the grants in the authority block below. Hyper confirmed the worker is reusable; no duplicate executor is created. |
| Accepting owner | Claude coordinator (3), "Coordinating parallel Claude sessions (3)" | Specification, conflict adjudication, the release record, acceptance of the return and combined acceptance. It does not take campaign ownership from the recorded campaign coordinator. |
| Relay and contact | Codex Coordinator 2, `01a0ff59-ac63-76a1-ab49-f9cd5515ff24` (desktop) | Relay and contact only; it accepts nothing. It performs the executive review (B3). |
| Operator | Joshua | The ratification reply (B14) and the merge go on the ratification PR, through the merge-order agent. |

**Owners this card narrows (it changes none of them):**
- Dot charter: [`docs/notes/2026-10-02-dot-deployment-responsibility.md`](../../notes/2026-10-02-dot-deployment-responsibility.md) at `main@152716dd90a995c2d5e533c9d41f38d42db31748` (#623).
- Seats, action classes, `IN_DOUBT`, committed-handoff rule: [surface-allocation ADR](../../adr/2026-07-14-cc-cursor-surface-allocation.md#action-classes-and-the-authority-block), Addenda 2026-09-26b and 2026-09-30b; registry [`scripts/seat_authority.yml`](../../../scripts/seat_authority.yml).
- Calendar ratification precedent: [`ops/calendars/README.md`](../../../ops/calendars/README.md) `:145-200`; [`ops/calendars/RATIFIED.json`](../../../ops/calendars/RATIFIED.json) (append-only rows); loader `ops/c1_rail/book_session_calendar.py` `load_ratifications` `:548-581` and `load_ratified_calendar` `:583-601`; October precedent PR #560.
- Trade-date gap owner: `docs/notes/2026-09-15-packet1-step4-session-calendar.md` `:122-131`.
- Commit gates: [`scripts/gates.yml`](../../../scripts/gates.yml) and `scripts/githooks/pre-commit`.

```yaml authority
seat: worker
parent: docs/notes/2026-10-02-dot-deployment-responsibility.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push, pr.open]
constraints:
  - no_main_write
  - no_merge
  - no_ratify
  - no_auto_merge
  - section2_three_files_only
  - no_calendar_or_evidence_byte_change
  - no_december_authoring
  - no_thanksgiving_recheck
  - no_handoff_or_subagent_dispatch
  - no_ci_or_cloud_dispatch
  - no_schedule_or_monitor_creation
  - no_spend_arm_deploy_or_trade
  - no_private_data_pine_or_ports
  - hook_proof_before_any_push
  - hook_proof_worktree_kept_and_never_pushed
  - b14_values_only_from_hyper_dispatch
  - record_url_read_from_opened_pr_never_predicted
  - independent_reviewer_only
  - comments_only_on_own_pr
  - in_doubt_inspect_before_retry
  - two_failed_corrections_escalate
  - return_to_hyper_until_coordinator_3_acknowledges
acceptance:
  - tests/ops/test_book_session_calendar.py::test_november_is_ratified_and_admits
  - tests/ops/test_book_session_calendar.py::test_checked_in_ratification_binds_exactly_the_checked_in_bytes
  - tests/ops/test_book_session_calendar.py::test_october_is_ratified_and_admits
  - tests/ops/test_book_session_calendar.py::test_defective_ratification_files_are_refused
  - tests/ops/test_book_session_calendar.py::test_november_calendar_and_evidence_are_byte_pinned_and_v2
  - tests/ops/test_book_session_calendar.py::test_november_reproduces_from_the_authoring_tool
  - tests/ops/test_book_session_calendar.py
  - tests/ops/test_account_close_assembler.py
  - tests/ops/test_book_settlement.py
  - tests/ops/test_account_close_calculation.py
```

**Seat choice (executor).** `worker` is the narrowest registry seat whose grant covers the five capabilities this assignment needs (`scripts/seat_authority.yml:105-108`: `max_risk: medium`, `grantable: [repository.read, tests.run, worktree.write, research.run, branch.push, pr.open, ci.dispatch]`). `escalation` (`:101-104`) and `coordinator` (`:96-100`) grant more; `executive` (`:93-95`) lacks `worktree.write`, `branch.push` and `pr.open`. The block grants exactly five: `repository.read` (`:37`, low), `tests.run` (`:38`, low), `worktree.write` (`:39`, low), `branch.push` (`:41`, medium; `codex/*` here, never `main`) and `pr.open` (`:42`, medium). It withholds the seat's `research.run` and `ci.dispatch`. The registry's name is `pr.open`; there is no `pr.create`. `worktree.write` is in `acceptance_required_for` (`:88`), so the block names its acceptance tests. The parent is the charter, which carries no authority block: it records provenance and narrows nothing beyond the seat (checker rule A7).

**Seat choice (hyper).** A card carries exactly one authority block (checker rule A1), and this one is the executor's. Hyper's narrowed grant is recorded in the table above and in B3, and was checked by hand against the same rules: both capabilities are registered, neither is `high`, both are grantable to `coordinator` (`:98-99`), and the ceiling is medium. `check_handoff_authority.py` binds grants to the declared seat only. Binding hyper to `coordinator` and the worker to `worker` is coordinator (3)'s pre-dispatch read plus the executive review (ADR Addendum 2026-09-26b).

**Grant gap, recorded rather than widened.** The registry has no comment capability. Under the contact routes accepted on 2026-10-03 (B5):
- The worker posts `[worker → coordinator (3)]` comments and the review request (`@codex review`) on **the ratification PR it opened**. These are read as part of `pr.open`.
- Hyper posts `[hyper → coordinator (3)]` comments on that PR as internal coordination under the charter's communication clause ("Communicate internally with the named coordinator and workers assigned to the released work"). This grants hyper no push, PR, review or approval.
- Neither reading covers review comments on any other PR (`pr.review`), an approval, or a comment anywhere else. Coordinator (3)'s release record on #622 is coordinator (3)'s own act.

**Residual (merge).** If the worker acts with Joshua's `gh` credential, which can merge, then "no merge" holds only by instruction. The `main` ruleset requires a PR and `skills (3.12)` but does not stop that credential from merging a green PR, and `scripts/guard_operator_acts.py` is a Claude Code hook that does not run on OpenAI surfaces.

## 0. Startup bindings (§0) and Phase-0 reads

§0.1 lists the startup bindings the charter (`docs/notes/2026-10-02-dot-deployment-responsibility.md`) requires before the first autonomous dispatch; §0.2 lists the Phase-0 reads the worker reports before any edit.

### 0.1 Startup bindings

The charter's *Activation and evidence of fitness* section requires these before the first autonomous dispatch. Values were observed on 2026-10-02 (America/New_York; 2026-10-03 UTC) from `origin/main@1a350ec3a60789eeebc8b8cc3d2eae5ab4f98c4d`, GitHub, and coordinator (3)'s relay of the 2026-10-03 binding acceptance; B3 and B15 were updated on 2026-10-03 from the B3 review and #622's merge commit. Nothing here was verified from hyper's or the worker's own surface. The card is released only when the B3 re-review of revision 3 is CLEAN; B15 is BOUND.

| # | Binding | Value | State |
|---|---|---|---|
| B1 | Adopted charter revision | `docs/notes/2026-10-02-dot-deployment-responsibility.md` at `152716dd90a995c2d5e533c9d41f38d42db31748` (#623, merged 2026-10-03T01:57:11Z). Joshua told Coordinator 2 directly: "I have adopted the deployment follow-through charter for hyper". The document's own Status line still reads "proposed responsibility wording"; adoption rests on his statement. | **BOUND.** Settled; do not ask again. |
| B2 | Dot identity | **hyper**, OpenAI dot, conversation `01a0ff79-c8a3-77b4-b0eb-83b11cce90f4`, durable host. | **BOUND.** |
| B3 | Seats and executive review | (a) hyper: `coordinator`, narrowed to `repository.read` plus `handoff.dispatch` for the one worker in (b); no direct execution. (b) Executor: worker `01a0ff7c-9b6e-70f7-96a8-8ea3f8a4b0d0` under `worker` with the five grants in the authority block. (c) Executive-review performer: **Codex Coordinator 2 (relay), independent of the drafter.** | **BOUND** (seats and performer, accepted 2026-10-03). Executive review **NOT CLEAN** at revision 2 (`524fcd12350b67528818c23751a9581098949d6e`; 2 P2, 1 P3, folded in revision 3). Revision 3 is **pending a focused re-review** by the same performer. The release record cites its CLEAN verdict at the revision-3 commit; without it the card is not released. |
| B4 | Accepting owner | Claude coordinator (3) owns acceptance and combined acceptance. Coordinator 2 is relay and contact only. | **BOUND.** |
| B5 | Contact routes | (a) hyper ↔ Coordinator 2: hyper posts `[hyper → Coordinator 2]` in its own chat; desktop Coordinator 2 (`01a0ff59-ac63-76a1-ab49-f9cd5515ff24`) reads it and replies with supported tools. A direct return to local Coordinator 2 failed with `CloudThreadNotFoundError`. (b) Decision updates for Joshua go in his existing hyper chat. (c) Coordinator (3) is reached through Coordinator 2, or through durable `[hyper → coordinator (3)]` / `[worker → coordinator (3)]` comments on the ratification PR once it exists. (d) The release record is a `[coordinator (3) → hyper]` comment on #622. (e) Hyper ↔ worker: hyper's dispatch and follow-up messages in the worker's task; the worker's returns to hyper there. | **BOUND.** |
| B6 | Recipients and access | (a) Repository `Joshua-Asante/first-passage` (public): the worker pushes `codex/*` branches and opens PRs. (b) The GitHub identity the worker acts as is reported at Phase 0 (item 6), login only; the merge residual above applies if it is Joshua's credential. (c) Surface: the worker's local host, because the card needs the operations launcher (`python -I scripts/fp.py`) and the installed git hooks; B13 proves the hooks there. (d) Hyper reaches coordinator (3) only through B5. (e) The *Grant gap* reading of comments. | **BOUND**; (b) is reported, not chosen. |
| B7 | Card | This file at its revision-3 commit on `claude/dot-card-calendar-ratification`. That commit is the dispatch revision. | BOUND on commit; the release record cites the SHA. |
| B8 | Budget and concurrency | One active worker, the one named in B3(b). Hyper dispatches it once. No second worker, subagent, scheduled task or cloud run; no new compute or spend: ordinary task usage within the existing allowance. CI runs only because of the worker's own pushes; `ci.dispatch` is not granted. | **BOUND.** |
| B9 | Write footprint | Branch `codex/dot-2026-11-calendar-ratification` (new, from `main`). Files: `ops/calendars/RATIFIED.json`, `ops/calendars/README.md`, `tests/ops/test_book_session_calendar.py`. Disjoint from every other released card now that #622, which wrote the same README and test file, has merged (B15). The B13 disposable worktree and its throwaway local branch are outside the PR, never pushed and kept. | **BOUND**; the serialisation behind #622 (§9) is discharged. |
| B10 | Evidence destination | `[worker → coordinator (3)]` comments on the ratification PR. Each carries the PR, the exact head (full 40-character SHA) and, for each launcher run, the `record.json` path with its `status`, `verification_exit_code`, `source_stable` and test counts, meeting §4's RED or GREEN expectations. Before the PR exists, the Phase-0 report and the hook proof go to hyper in the worker's task and are repeated in the first PR comment. | **BOUND.** |
| B11 | Notification owner | Hyper, to Joshua's existing hyper chat, for decisions (B14, the final decision packet) and outcomes, in the charter's update format. Coordination goes to Coordinator 2, then coordinator (3). | **BOUND.** |
| B12 | Monitoring | Consolidated Codex Coordinator 2 (`01a0ff59-ac63-76a1-ab49-f9cd5515ff24`) is relay and contact (B5). Hyper's own supported wake behaviour is the sole owner of follow-through on this card, without a timing guarantee. No new monitor or schedule. Coordinator 1 (`01a0fa4b…`) is archived and is not a recipient. | **BOUND.** |
| B13 | Hook proof (surface controls) | `git commit --dry-run` does not run hooks and is not evidence. Before any push, the worker validates the actually configured hooks in a fresh, uniquely named disposable worktree on a throwaway local branch that is never pushed (§3, worker step 2): (1) `git config core.hooksPath` and the hook files; (2) a real commit the pre-commit `staged-debris` gate refuses, with its refusal output; (3) a clean real commit, with the hook's pass output. The disposable worktree and branch are not deleted; their path is reported. Revision 1's host-side observation stands: `core.hooksPath` = `C:\Users\joshu\multi_firm_operations\.git\hooks`, shared by worktrees. | **BOUND** (procedure); evidence owed by the worker before any push. Hooks not running on the worker's surface is a STOP: `NEEDS_CONTEXT`. |
| B14 | Ratification row values `NOV_INSTRUCTION` and `NOV_RATIFIED_UTC` | Joshua has **not** ratified November. Coordinator (3)'s sheet 2 said "You ratify the digest when #622 is clean"; that describes his future act, not a ratification, so asking now is a new act, not a repeated question. After #622 merges and the release record is posted, hyper sends Joshua, in his existing hyper chat, this one-line decision packet: "Ratify the November 2026 book session calendar, digest b89562a58a665daa4054f310f41007f815bb45b54444c6404ad463ac0b60aad7 (merged in #622 at <merge sha>)? Reply: ratify calendar b89562a5". Joshua's reply supplies `NOV_INSTRUCTION` verbatim. `NOV_RATIFIED_UTC` is the reply's timestamp, read in UTC to the second from the hyper chat by hyper or Coordinator 2. It must be ≥ `generated_utc` `2026-10-03T01:03:53Z` and before coverage end `2026-11-30T22:00:00Z` (README `:168-171` at `a5ca41e`, the generation/ratification ordering rule; loader `:599-600`). Both precedents (September `ratify calendar 650e8aab`; October, PR #560) recorded Joshua's instruction first. | **BOUND** (procedure; owners hyper for the packet, Joshua for the reply). Values are supplied at flow step 3. A reply that does not ratify digest `b89562a5` is not B14: hyper holds and reports to coordinator (3). |
| B15 | Prerequisite | PR #622 (`claude/calendar-2026-11`) is **MERGED** at `8de2e6357c3b3ad3e137737fc3c5fb40dfca36fe` (2026-10-03T03:25:15Z), an ancestor of `origin/main`. The calendar digest recomputed at the merge commit is `b89562a58a665daa4054f310f41007f815bb45b54444c6404ad463ac0b60aad7`; overlay `483f2324b85548e60429b823454641a0ee6e34c8ef2a9cadc7dcc6555f7def5b` on `main`. Not ratified: `RATIFIED.json` at `8de2e63` has no row for that digest. | **BOUND.** |

### 0.2 Phase-0 reads (read-report-before-code)

The worker reports these to hyper before any edit, and repeats them in the first PR comment. Bounce `NEEDS_CONTEXT` to hyper on any contradiction.

1. **Premise.** #622 is MERGED. Its merge commit is an ancestor of `origin/main`. On `origin/main`, `sha256(ops/calendars/book_session_calendar_2026-11.json)` = `b89562a58a665daa4054f310f41007f815bb45b54444c6404ad463ac0b60aad7` and `NOV_CALENDAR_SHA256` in the test file equals it. If either differs, the prerequisite has changed (§7).
2. **Release and dispatch.** The `[coordinator (3) → hyper]` release record exists on #622, cites this card's revision-3 SHA and gives B-row values matching §0.1. Hyper's dispatch gives `NOV_INSTRUCTION`, `NOV_RATIFIED_UTC` and the reference of Joshua's reply in the hyper chat. `NOV_RATIFIED_UTC` is ≥ `2026-10-03T01:03:53Z`, before `2026-11-30T22:00:00Z` and after #622's `mergedAt`. Without all of these, stop.
3. **Reads.** Read these in full: `ops/calendars/RATIFIED.json`; `ops/calendars/README.md` `:145-200`; `ops/c1_rail/book_session_calendar.py` `:548-601`; and in `tests/ops/test_book_session_calendar.py`, `test_checked_in_ratification_binds_exactly_the_checked_in_bytes`, `test_october_is_ratified_and_admits`, `test_defective_ratification_files_are_refused` and the November block added by #622. Also read PR #560's diff as the precedent.
4. **Existing work.** Search GitHub for an existing branch or PR for this ratification (`gh pr list --state all --search "b89562a5"`, `git ls-remote origin 'refs/heads/codex/dot-*'`). Reuse what exists; never create a duplicate (§8).
5. **Test 0, vendor bytes and secrets.** This card reads no gitignored vendor-data path, no `.env`, no secret, no Pine and no runtime port. None is staged for this dispatch, and none is needed. Account identifiers and private figures stay out of every message and comment.
6. **Identity.** Report `gh api user -q .login` and `git config user.name`, never a token. If the login can merge on this repository, the merge residual applies and is restated in the return.

## 0.5. Clarifying questions and routing

- **Routing.** This is a frozen, precedented, three-file follow-through, so the worker seat suffices for the executor (routing test 2). It authors no doctrine and touches no locked or `core/` anchor surface (test 1). Hyper routes the released card to its assigned executor (charter: "Otherwise route the work to its assigned executor"). Ratification and merge are operator acts (`governance.ratify`, `pr.merge`, both `high`), left to Joshua.
- **Owed before release:** a CLEAN B3 focused re-review of revision 3. B15 is BOUND. B14 is obtained after release (flow step 3), by its own procedure. A question that comes up during execution goes to hyper as `NEEDS_CONTEXT`; neither hyper nor the worker resolves it alone, and hyper takes it to coordinator (3) through B5.
- **Scope note.** Appending the November row makes #622's `test_november_is_not_ratified` fail, and `test_checked_in_ratification_binds_exactly_the_checked_in_bytes` pins the ratified set. PR #560 edited the test file for the same reason. The footprint therefore includes `tests/ops/test_book_session_calendar.py`, limited to the §2 edits.

## 1. Selected outcome

A PR from `codex/dot-2026-11-calendar-ratification` against `main` appends the operator ratification row for November digest `b89562a5…` to `RATIFIED.json`, using the values from Joshua's B14 reply. It changes the README's November row to "ratified" and records Joshua's sheet-2 acceptances, and it swaps the test's not-ratified assertion for a ratified-and-admits assertion. An independent reviewer reports CLEAN at one exact head, the worker returns to hyper, and hyper returns to coordinator (3). The PR is not merged by any agent; Joshua's merge go is his operator act.

Joshua's sheet-2 acceptances to record, as given by the operator directly to coordinator (3) on 2026-10-02 ("all recommended" on sheet 2 item 2):
- The 2026-11-26 row's `cme_trade_date` 2026-11-26 is accepted explicitly as-is. CME puts that session in trade date 2026-11-27, and the authoring tool has no trade-date input. He accepted September's Labor Day row the same way.
- 2026-11-11 DENIED `MISSING_SOURCE` is accepted.
- 2026-11-25 and 2026-11-30 PERMITTED are accepted.
- A Thanksgiving re-check on or after 2026-11-12 is owed (**owner: coordinator (3)**; outside this card). A changed byte means a new digest and a new decision.

Sheet 2's "You ratify the digest when #622 is clean" described Joshua's future act. It is not a ratification and supplies no row values; B14 obtains the act.

## 2. Scope (exact edits; nothing else)

1. **`ops/calendars/RATIFIED.json`:** append one object to `ratifications`, after the October row. Edit no existing row, and keep the file's existing 2-space JSON formatting and trailing newline (write LF bytes). The keys are exactly the loader's `_RATIFICATION_KEYS`:
   - `calendar_id`: `tradeify-select-100k/forward/2026-11`
   - `calendar_file`: `ops/calendars/book_session_calendar_2026-11.json`
   - `calendar_sha256`: `b89562a58a665daa4054f310f41007f815bb45b54444c6404ad463ac0b60aad7`
   - `closure_overlay_file`: `ops/calendars/book_closure_overlay.json`
   - `closure_overlay_sha256`: `483f2324b85548e60429b823454641a0ee6e34c8ef2a9cadc7dcc6555f7def5b`. Recompute it from `main` and stop if it differs.
   - `coverage_start_utc`: `2026-10-28T22:00:00Z`; `coverage_end_utc`: `2026-11-30T22:00:00Z`. Both come from the calendar's `coverage` block.
   - `ratified_by`: `operator`
   - `ratified_utc`: B14 `NOV_RATIFIED_UTC`; `instruction`: B14 `NOV_INSTRUCTION`, verbatim
   - `record`: the URL of the ratification PR, read from GitHub after the PR is opened (§3 worker step 6). Never predicted, never a placeholder: rows are append-only, so a wrong URL is permanent once merged.
   - `scope`: "Book permission rows for the November 2026 monthly extension, including the 2026-10-29 and 2026-10-30 rollover overlap rows, as authored: 2026-11-11 DENIED (MISSING_SOURCE), 2026-11-26 DENIED (HOLIDAY), 2026-11-27 DENIED (SHORTENED); 2026-11-25 and 2026-11-30 PERMITTED accepted; the 2026-11-26 row's cme_trade_date 2026-11-26 accepted by the operator as-is (CME trade date 2026-11-27; authoring tool has no trade-date input); Thanksgiving halts provisional, re-check on or after 2026-11-12 owed and any changed byte is a new digest and a new decision. Grants no activation, deployment, resumption or historical legality."
2. **`ops/calendars/README.md`:** the single ratification row edit, following the October precedent (#560's October row). Only the November table row added by #622 (`:149` at `8de2e63`) changes, by exactly these two substitutions, where `<D>` is the UTC date (`YYYY-MM-DD`) of `NOV_RATIFIED_UTC`:
   ```text
   old lead: **Candidate, not ratified (digest `b89562a5…`).**
   new lead: **Ratified by the operator (<D>, digest `b89562a5…`).**
   old end:  (the trade-date input gap below). |
   new end:  (the trade-date input gap below). Operator acceptances: the 2026-11-26 `cme_trade_date` as-is, 2026-11-11 `MISSING_SOURCE`, and 2026-11-25 and 2026-11-30 `PERMITTED`; the Thanksgiving re-check stays owed. Admission starts at the row's `ratified_utc`. |
   ```
   Admission boundaries: `git diff --numstat origin/main...HEAD -- ops/calendars/README.md` reads `1 1`; every other byte of the row, the ⚠ trade-date sentence included, is unchanged; no other README line changes; no ratified text (the September and October rows, the "Monthly extension" paragraph) is reworded.
3. **`tests/ops/test_book_session_calendar.py`:**
   - Inside the November block, beside `NOV_CALENDAR_SHA256`, add two module-level literals: `NOV_INSTRUCTION` (B14's text, verbatim) and `NOV_RATIFIED_UTC` (B14's instant, `YYYY-MM-DDTHH:MM:SSZ`).
   - In `test_checked_in_ratification_binds_exactly_the_checked_in_bytes`, change the set to `{CALENDAR_SHA256, OCT_CALENDAR_SHA256, NOV_CALENDAR_SHA256}`. The docstring sentence becomes: the October and November rows are the only other ratifications, checked in their own tests.
   - Replace `test_november_is_not_ratified` with `test_november_is_ratified_and_admits`, asserting exactly:
     - (i) the raw load `load_november().session_for(et(2026, 11, 16, 9)).refusal == "calendar_not_ratified"`;
     - (ii) the row read as `load_ratifications(RATIFIED)[NOV_CALENDAR_SHA256]` has `closure_overlay_sha256 == OVERLAY_SHA256`, `ratified_by == "operator"`, `instruction == NOV_INSTRUCTION`, `ratified_utc == NOV_RATIFIED_UTC`, and coverage `("2026-10-28T22:00:00Z", "2026-11-30T22:00:00Z")`;
     - (iii) `load_ratified_calendar(NOV_CALENDAR, …)` has `calendar_digest == NOV_CALENDAR_SHA256`, and `ratified_at` equals `NOV_RATIFIED_UTC` parsed as UTC;
     - (iv) `session_for(et(2026, 11, 16, 9), expected_digest=NOV_CALENDAR_SHA256).permitted`, and the same for 2026-11-25 and 2026-11-30 at 09:00 ET;
     - (v) the refusals for 11-11, 11-26 and 11-27 at 09:00 ET are `session_denied:MISSING_SOURCE`, `session_denied:HOLIDAY` and `session_denied:SHORTENED`;
     - (vi) in the raw file, the 2026-11-26 row's `cme_trade_date` is `2026-11-26` for all four products, which pins the accepted defect so that a re-author is visible.
   - No other test changes. A further test that fails because of the appended row is a §7 stop, not a licence to edit it.
   - The executor writes this primary acceptance test itself, so it is not the acceptance basis alone (ADR handoff-contract item 5): coordinator (3) checks its body against (i)–(vi) and the row and literals against B14 at acceptance, and the pre-existing named tests carry the rest.

## 3. Flow and method

**Flow (in order; each step waits for the one before it).**

| Step | Act | Owner |
|---|---|---|
| 1 | #622 merges with digest `b89562a5` (prerequisite, B15): done at `8de2e63` | Joshua |
| 2 | Release record: `[coordinator (3) → hyper]` comment on #622 citing this card's revision-3 SHA, the B-row values and the CLEAN executive re-review verdict (B3) | coordinator (3) |
| 3 | B14 ratify packet to Joshua in his hyper chat; wait for his reply; read `NOV_INSTRUCTION` and `NOV_RATIFIED_UTC` | hyper (Coordinator 2 may read the timestamp) |
| 4 | Dispatch the named worker once, with this card's revision-3 SHA, the release-record URL, the B14 values and the reply reference | hyper |
| 5 | Phase 0, hook proof, commit 1, push, PR, commit 2, green runs (worker steps 1–8 below) | worker |
| 6 | Independent review: `@codex review` or a relay reviewer independent of coordinator (3) and of this card's drafter, with the verdict posted on the PR naming the full head SHA | reviewer; requested by the worker |
| 7 | Worker returns to hyper; hyper inspects the evidence and returns to coordinator (3); coordinator (3) acknowledges | worker, hyper, coordinator (3) |
| 8 | Joshua's merge go on the ratification PR, through the merge-order agent | Joshua (operator act, outside this card) |

After coordinator (3) records RESOLVED, hyper sends Joshua the decision packet (§6) in his hyper chat.

**Worker method.**
1. **Phase 0** (§0.2), reported to hyper.
2. **Hook proof (B13), before any push.** Create a fresh, uniquely named disposable worktree on a throwaway local branch from `origin/main`, for example `git worktree add -b hookproof/dot-card-01-<UTC stamp> <new path>/hookproof-dot-card-01-<UTC stamp> origin/main`. Inside it:
   - (1) Report `git config core.hooksPath` and list the hook files in that directory (if unset, `git rev-parse --git-path hooks`).
   - (2) **Expected refusal.** Write a one-line root file `tmp-hook-proof.txt`, `git add tmp-hook-proof.txt`, then `git commit -m "hook proof: expected refusal"`. The pre-commit hook (`scripts/githooks/pre-commit:7`, `gate_manifest.py --tier pre-commit`) runs the `staged-debris` gate (`scripts/gates.yml:458-462`, tier `always`), which refuses any staged root-level `tmp-*` path (`scripts/check_staged_debris.py` docstring). Record the full refusal output and show that `git log -1` is unchanged. Then `git restore --staged tmp-hook-proof.txt`; the file stays.
   - (3) **Expected pass.** Write a one-line root file `hook-proof-clean.txt`, `git add hook-proof-clean.txt`, then `git commit -m "hook proof: clean"`. Record the hook's pass output and the new commit SHA.
   - Do not delete the disposable worktree, its branch or its files; never push the branch. Report the path and branch name.
   - If step (2) creates a commit, or no hook output appears in (2) or (3), hooks do not run on this surface: STOP, push nothing and return `NEEDS_CONTEXT`. If (3) is refused by a gate that also fails on unmodified `origin/main`, return `BLOCKED` with the output; committing without hooks is forbidden.
3. **Worktree.** Cut a new, uniquely named worktree on `codex/dot-2026-11-calendar-ratification` from `origin/main`.
4. **Commit 1, the fail-first record.** Make the §2.2 README edit and the §2.3 test edits (literals included). Run `python -I scripts/fp.py python -m pytest tests/ops/test_book_session_calendar.py::test_november_is_ratified_and_admits`: its launcher record must be §4's RED record (`status: failed`, non-zero `verification_exit_code`, `source_stable: true`, the expected `KeyError` at the row lookup in (ii)). Run `git diff --stat`, then commit with the hooks active.
5. **Push and open the PR.** Push the branch. Open the PR; its body states it is **not ratified until Joshua's act**, cites this card's revision-3 SHA and the B14 reply reference, and says a second commit appends the row.
6. **Read the PR number from GitHub** (`gh pr view codex/dot-2026-11-calendar-ratification --json number,url`). Never predict it.
7. **Commit 2.** Append the §2.1 row with `record` set to that URL. Run the launcher on `tests/ops/test_book_session_calendar.py`, then on `tests/ops/test_account_close_assembler.py tests/ops/test_book_settlement.py tests/ops/test_account_close_calculation.py`, then `python -I scripts/fp.py check`. Run `git diff --stat`, commit with the hooks active, and push.
8. **Evidence and review.** Post the first `[worker → coordinator (3)]` PR comment: Phase-0 report, hook proof, both commits' SHAs and every launcher record. Request `@codex review`, or the relay reviewer coordinator (3) names through Coordinator 2, who must be independent of coordinator (3) and of this card's drafter. Fix in-scope findings within §2, re-run the affected checks and re-request review, until CLEAN at one exact head. Then return to hyper (§6).

**Hyper method.** Steps 3, 4 and 7 of the flow. Before step 7's return, inspect the actual diff and launcher records (charter step 5): tested revision, `status`, exit result, `source_stable` against §4's RED and GREEN expectations, and the reviewed head. A worker DONE without that evidence is not promoted. Return through a `[hyper → coordinator (3)]` comment on the PR and a `[hyper → Coordinator 2]` message in hyper's own chat.

## 4. Verification (falsifier-first)

**H:** appending exactly this row, with these three file edits, makes the November digest admissible from `NOV_RATIFIED_UTC` and leaves September and October admission and every other calendar and account-close test unchanged.

**Reject if** (falsifier):
- any named acceptance test fails at the return head;
- `fp check` exits non-zero, apart from a pre-existing failure shown to fail identically on `main`, disclosed and not counted as a pass;
- the diff touches a file or line outside §2;
- an existing `RATIFIED.json` row's bytes change;
- the calendar or evidence digests differ from §0.2 item 1;
- the row's `instruction` or `ratified_utc` differs from B14, or `record` is not the PR's own URL;
- the hook proof (B13) is missing or was not made before the first push;
- a launcher record does not meet the RED or GREEN expectations below.

**Launcher record expectations.** The recorder sets `status: failed` for every non-zero exit (`scripts/record_verification.py:299-300`), so `completed` with a non-zero exit cannot occur.
- **RED (fail-first, commit 1).** Before the row is appended, the `test_november_is_ratified_and_admits` record is a captured expected failure: `status: failed`, non-zero `verification_exit_code`, `source_stable: true`, and the failure is the expected `KeyError` at the row lookup in (ii). Any other failure is not RED evidence. A test that cannot be made to fail before the append is a §7 stop.
- **GREEN (acceptance).** Every return-head pytest record: `status: completed`, `verification_exit_code: 0`, `source_stable: true`. The `fp check` record meets the same, except a pre-existing failure under the second reject bullet, which is disclosed with its `failed` record and not counted as a pass.

**Revert trigger:** any admission decision for a September or October instant differs from `main`. The return-head runs of `tests/ops/test_book_session_calendar.py` and the three account-close test files cover it.

Return-head evidence:
- the full `tests/ops/test_book_session_calendar.py` GREEN launcher record (the same count as `main` after #622, since the swap is one-for-one);
- the GREEN launcher record for `tests/ops/test_account_close_assembler.py`, `tests/ops/test_book_settlement.py` and `tests/ops/test_account_close_calculation.py`;
- the `fp check` record;
- `git diff --check`;
- `git diff --stat origin/main...HEAD` showing exactly three files;
- `required skills (3.12)` green at the exact head.

## 5. Forbidden

- Merging, auto-merge, approving the PR or pushing to `main`.
- Describing the calendar as ratified anywhere except the proposed `RATIFIED.json` row and the §2.2 README row edit; any other prose edit, including rewording ratified text.
- Editing `book_session_calendar_2026-11.json`, any evidence file, the overlay, the October or September files, or any existing `RATIFIED.json` row.
- Re-authoring the calendar, the Thanksgiving re-check, December authoring, or any trade-date-input build.
- `core/`, `lab/`, Pine, runtime ports, `ops/c1_rail/**` code, `scripts/**`, `.claude/**`, `AGENTS.md`, `STATE.md`, ledgers, ADRs and campaign records.
- **Hyper:** any worktree write, test run, push, PR or review; dispatching any worker other than `01a0ff7c-9b6e-70f7-96a8-8ea3f8a4b0d0`, or that worker twice; obtaining B14 values from anything but Joshua's reply.
- **Worker:** dispatching workers, subagents, CI workflows or cloud runs; inventing, back-dating or paraphrasing B14 values.
- Creating schedules or monitors; any spend, arm, deploy or trade action.
- `git commit --no-verify`, `git commit --dry-run` as hook evidence, `git stash`, pushing the hook-proof branch, force-push to a branch the worker did not create, and deleting any branch, PR, comment or worktree (the hook-proof worktree included).
- Committing or quoting account identifiers, P&L, vendor CSVs, Pine or ports.
- Contacting anyone outside the B5 routes and the named reviewer.

## 6. Output and return (status taxonomy)

The worker returns **DONE**, **DONE_WITH_CONCERNS**, **NEEDS_CONTEXT** or **BLOCKED** to hyper in its task and as a `[worker → coordinator (3)]` PR comment once the PR exists. Hyper returns it to coordinator (3) through B5. Coordinator (3)'s verdict is **RESOLVED** (every §4 item holds at the return head) or **FALSIFIED** (a named item fails; returned to hyper for the worker). The return contains:
- the PR number and URL, the exact head SHA (40 characters) and the base SHA;
- `git diff --stat` plus the full diff;
- the launcher `record.json` paths with `status`, `verification_exit_code`, `source_stable` and the counts (the fail-first RED record and the return-head GREEN records, §4);
- the CI status at the head;
- the reviewer's identity, its verdict URL and the full head SHA it reviewed;
- the Phase-0 report, including the GitHub login and, if it can merge, the merge residual;
- the hook proof: `core.hooksPath`, the hook files, the refusal output, the pass output with its commit SHA, and the disposable worktree path and branch;
- `NOV_INSTRUCTION`, `NOV_RATIFIED_UTC` and the reference of Joshua's reply;
- every `IN_DOUBT` event and how it was reconciled;
- concerns;
- the decision packet hyper sends Joshua after RESOLVED, one line: `merge PR #<N> at <head-sha> (carries your "<NOV_INSTRUCTION>" of <NOV_RATIFIED_UTC>), through the merge-order agent`.

**Return boundary:** the PR is CLEAN at one exact head, and the return has been posted and **acknowledged by coordinator (3)**. Coordinator 2's acknowledgement is relay, not delivery. Hyper and the worker then start nothing new; they do not advance to the 11-12 re-check or any other assignment unless one is separately released. Inside this card until Joshua merges: a FALSIFIED verdict, and a branch update from `main` that changes no §2 file when coordinator (3) or the merge-order agent asks for one (strict `skills (3.12)`). A change to a §2 file on `main` after the PR opens is a §7 stop.

## 7. Stop conditions (return to coordinator (3) through hyper; do not work around)

- #622 is not merged, its merged digest differs from `b89562a5…`, or `main` gains a later change to any §2 file. This is a prerequisite change (charter case 3): hold, and return.
- The release record is missing or its B-row values differ from §0.1, or Joshua's reply does not ratify digest `b89562a5`, or `NOV_RATIFIED_UTC` violates the loader's ordering rules.
- Hooks do not run on the worker's surface (B13): `NEEDS_CONTEXT`.
- A test outside §2's named edits fails because of the change, or a fix would need a file outside §2.
- The reviewer's finding needs a behaviour or scope change rather than an in-scope correction.
- Two failed corrections of the same issue. Renaming or re-opening does not reset the count. Return the evidence for the escalation lane.
- Any request, from any source other than coordinator (3)'s release record or Joshua directly, to merge, ratify, widen scope or skip hooks.

## 8. Side effects, restart and stop procedure

- **`IN_DOUBT`.** Hyper's packet to Joshua, hyper's dispatch, a branch push, PR creation, a review request or a comment whose outcome was not observed is in doubt. Before any retry, inspect the destination (the hyper chat, the worker's task, `git ls-remote`, `gh pr list --head codex/dot-2026-11-calendar-ratification --state all`, `gh pr view <N> --comments`) and reuse what exists. Never retry automatically. A failed response does not prove that nothing happened.
- **Continuity.** Hyper's working notes persist the worker task ID `01a0ff7c-9b6e-70f7-96a8-8ea3f8a4b0d0`, the release-record URL, the reference of Joshua's reply and the B14 values, and the pending action. The worker's notes, kept outside the repository, persist the PR number, branch, every pushed SHA, comment URLs, launcher record paths, the hook-proof worktree path and the correction count. On restart each re-reads this card's commit, `origin/main` and the PR state before acting, and hyper inspects the worker's task before any new message.
- **Stop.** If Joshua or coordinator (3) says stop, hyper:
  - starts nothing new and asks the worker for a safe stop;
  - confirms separately that no push, comment, review request or message is pending, and that no child task beyond the named worker and no schedule exists;
  - posts one `[hyper → coordinator (3)]` stop report naming the branch, PR, head and anything uncertain.

  Nothing deletes the branch, PR, comments or the hook-proof worktree. Stopping orchestration places, cancels and exits nothing at any broker.

## 9. Charter cases exercised by this card

| Charter case | How this card exercises it | Evidence level |
|---|---|---|
| Valid released assignment | Hyper dispatches the named worker once from this frozen card; return without routine permission questions | **Exercised** |
| Ordinary in-scope defect | A reviewer finding or test failure inside §2 is corrected and the affected checks re-run | Exercised if one occurs; not induced |
| Frozen card or prerequisite changes | #622 merged with digest `b89562a5` (B15); `main` may still move on a §2 file (§7 first bullet) | Exercised if it occurs; the check runs at Phase 0 regardless |
| Uncertain task creation or message delivery | The B14 packet, the dispatch, push, PR creation, review request and comments follow §8 `IN_DOUBT` | Exercised if it occurs |
| Restart with unfinished work | §8 continuity: hyper holds the saved worker task ID and pending action | Exercised only if hyper or the worker restarts mid-card; not induced |
| Concurrent assignments | The footprint collides with #622 (README, test file), so the card is **serialised** behind it; one active worker | **Exercised by construction** (serialise branch). The parallel branch is not exercised |
| Local computer unavailable | Launcher records and B13 need the worker's local host. If it is unavailable, mark local evidence unavailable, continue only GitHub-side preparation and return `BLOCKED` or `DONE_WITH_CONCERNS`, never DONE | Exercised if it occurs |
| Worker reports success without required evidence | Hyper inspects the records and the reviewed head before returning; a "clean" on a different head is not CLEAN | **Exercised** at return |
| Specification conflict or repeated failed corrections | §7 stops and the two-correction rule | Exercised if it occurs |
| Stop request | §8 stop procedure | Not exercised unless a stop is issued |
| Attempt to exceed authority | The assignment ends where Joshua's acts begin (ratification reply, merge). Hyper prepares the packets and defers the acts | **Exercised by construction** |

Not exercised by design: parallel allocation, schedules and subscriptions, attended-session preparation and closeout.

## 10. Audit hooks (runnable)

```bash
# Card form and authority, through the launcher. Expected: RESULT: well-formed; 0 violation(s).
python -I scripts/fp.py python scripts/check_brief.py --type handoff docs/briefs/handoffs/2026-10-02-dot-card-01-calendar-ratification.md
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-02-dot-card-01-calendar-ratification.md
# Prerequisite (Phase 0). Expected: MERGED and a merge SHA, then the November digest and the overlay digest.
gh pr view 622 --json state,mergeCommit,mergedAt -q '.state + " " + .mergeCommit.oid + " " + .mergedAt'
git show origin/main:ops/calendars/book_session_calendar_2026-11.json | sha256sum   # b89562a5...0aad7
git show origin/main:ops/calendars/book_closure_overlay.json | sha256sum            # 483f2324...def5b
# Release record. Expected: one [coordinator (3) → hyper] comment citing the revision-3 SHA.
gh pr view 622 --comments | grep -n "coordinator (3) → hyper"
# Hook proof (B13), inside the disposable worktree. Expected: refusal by staged-debris, then a pass.
git config core.hooksPath
git commit -m "hook proof: expected refusal"   # after staging root tmp-hook-proof.txt
git commit -m "hook proof: clean"              # after unstaging it and staging hook-proof-clean.txt
# No duplicate work (IN_DOUBT). Expected: empty before first creation.
gh pr list --state all --search "b89562a5 in:title,body"
git ls-remote origin 'refs/heads/codex/dot-2026-11-calendar-ratification'
# Scope at return. Expected: exactly the three section-2 files; no whitespace errors.
git diff --stat origin/main...HEAD
git diff --check origin/main...HEAD
# Acceptance at the return head.
python -I scripts/fp.py python -m pytest tests/ops/test_book_session_calendar.py
python -I scripts/fp.py python -m pytest tests/ops/test_account_close_assembler.py tests/ops/test_book_settlement.py tests/ops/test_account_close_calculation.py
python -I scripts/fp.py check
```
