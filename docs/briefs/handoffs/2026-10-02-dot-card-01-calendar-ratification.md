# Dot card 01: November 2026 calendar ratification follow-through

**Type:** cc_handoff (dot release card; the first released assignment under the dot charter)

**Status:** RELEASE-READY (frozen) — released when startup bindings §0 are complete and #622 is merged.
- Released by: Claude coordinator (3) ("Coordinating parallel Claude sessions (3)"), subject to every §0 row reading BOUND.
- Committed before any execution under the committed-handoff rule. The release record (who released it, at which commit of this card, with which §0 values) is a `[coordinator (3) → dot]` comment on the PR or the coordinator's own owner record; this file is not edited to record the release. A change to any frozen section is a new card.

**Executor:** the OpenAI dot named in §0 row B2, acting directly as the single writer (charter: "Direct implementation is permitted only when the dot is assigned that executor role and its card allows the change"). It dispatches no worker and no subagent.

**Accepting coordinator:** Claude coordinator (3). It owns the specification, conflict adjudication, acceptance of the return and the decision packet's delivery to Joshua.

**Coordination contact:** Codex Coordinator 2 (Codex chat ID `01a0ff59-ac63-76a1-ab49-f9cd5515ff24`). The dot cannot message Claude sessions directly. Its durable channel to coordinator (3) is a GitHub comment on the PR it opens, prefixed `[dot → coordinator (3)]`; the contact relays when a chat message is needed.

**Owners this card narrows (it changes none of them):**
- Dot charter: [`docs/notes/2026-10-02-dot-deployment-responsibility.md`](../../notes/2026-10-02-dot-deployment-responsibility.md) at `main@152716dd90a995c2d5e533c9d41f38d42db31748` (#623).
- Seats, action classes, `IN_DOUBT`, committed-handoff rule: [surface-allocation ADR](../../adr/2026-07-14-cc-cursor-surface-allocation.md#action-classes-and-the-authority-block), Addenda 2026-09-26b and 2026-09-30b; registry [`scripts/seat_authority.yml`](../../../scripts/seat_authority.yml).
- Calendar ratification precedent: [`ops/calendars/README.md`](../../../ops/calendars/README.md) `:145-200`; [`ops/calendars/RATIFIED.json`](../../../ops/calendars/RATIFIED.json) (append-only rows); loader `ops/c1_rail/book_session_calendar.py` `load_ratifications` `:548-581` and `load_ratified_calendar` `:583-601`; October precedent PR #560.
- Trade-date gap owner: `docs/notes/2026-09-15-packet1-step4-session-calendar.md` `:122-131`.

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
  - comments_only_on_own_pr
  - in_doubt_inspect_before_retry
  - two_failed_corrections_escalate
  - stop_at_coordinator_return
acceptance:
  - tests/ops/test_book_session_calendar.py::test_november_is_ratified_and_admits
  - tests/ops/test_book_session_calendar.py::test_checked_in_ratification_binds_exactly_the_checked_in_bytes
  - tests/ops/test_book_session_calendar.py::test_october_is_ratified_and_admits
  - tests/ops/test_book_session_calendar.py::test_defective_ratification_files_are_refused
  - tests/ops/test_book_session_calendar.py::test_november_calendar_and_evidence_are_byte_pinned_and_v2
  - tests/ops/test_book_session_calendar.py::test_november_reproduces_from_the_authoring_tool
  - tests/ops/test_book_session_calendar.py
```

**Seat choice.** `worker` is the narrowest registry seat whose grant covers the five capabilities this assignment needs (`scripts/seat_authority.yml:105-108`: `max_risk: medium`, `grantable: [repository.read, tests.run, worktree.write, research.run, branch.push, pr.open, ci.dispatch]`). `escalation` (`:101-104`) and `coordinator` (`:96-100`) grant more; `executive` (`:93-95`) lacks `worktree.write`, `branch.push` and `pr.open`. The card grants exactly five (`:37` `repository.read` low, `:38` `tests.run` low, `:39` `worktree.write` low, `:41` `branch.push` medium, `:42` `pr.open` medium) and withholds the seat's `research.run` and `ci.dispatch`. The registry's name is `pr.open`; there is no `pr.create`. `worktree.write` puts the card under `acceptance_required_for` (`:88`), so it names its acceptance tests above. `check_handoff_authority.py` binds these grants to the declared seat only; binding the seat to the dot is coordinator (3)'s pre-dispatch read plus the executive review (ADR Addendum 2026-09-26b). The parent is the charter, which carries no authority block: it records provenance and narrows nothing beyond the seat (checker rule A7).

**Grant gap, recorded rather than widened.** The registry has no comment capability. This card reads the `[dot → coordinator (3)]` return comments and the Codex review request (`@codex review`) on **the PR the dot opened** as part of `pr.open`. Review comments on any other PR (`pr.review`) are not granted. Coordinator (3) confirms this reading at release (§0 row B6) or narrows delivery to the PR body.

## 0. Startup bindings (§0) and Phase-0 reads

§0.1 lists the startup bindings the charter (`docs/notes/2026-10-02-dot-deployment-responsibility.md`) requires before release; §0.2 lists the Phase-0 reads the dot reports before any edit.

### 0.1 Startup bindings

The charter's *Activation and evidence of fitness* section requires these before the first autonomous dispatch. The card is released only when every row reads BOUND. Values were observed on 2026-10-02 (America/New_York) from `origin/main@152716d`, GitHub and the coordinator's relay. Nothing here was verified from the dot's own surface.

| # | Binding | Current value | State |
|---|---|---|---|
| B1 | Adopted charter revision | `docs/notes/2026-10-02-dot-deployment-responsibility.md` at `152716dd90a995c2d5e533c9d41f38d42db31748`. GitHub shows #623 merged by `Joshua-Asante` at 2026-10-03T01:57:11Z. Joshua's words, as relayed by Codex Coordinator 2 from chat `01a0ff36-f114-7653-ab9f-2e63b0652872`: "merge it, i will start up the dot". The document's own Status line still reads "proposed responsibility wording". | **PARTIAL — owner: coordinator (3).** Record Joshua's adoption directly, not through the relay alone: either his confirmation that the merge adopts the charter for this dot, or his words read in the source chat. |
| B2 | Dot identity | Not yet created. Joshua said he will start it. | **MISSING — owner: Joshua** (name and ID of the dot, recorded by coordinator (3)). |
| B3 | Seat | `worker`, with the five grants in the authority block (see *Seat choice*). | **PROPOSED — owner: coordinator (3)** (pre-dispatch read binding the seat to B2; executive review per Addendum 2026-09-26b). |
| B4 | Accepting owner | Claude coordinator (3), "Coordinating parallel Claude sessions (3)". It does not take campaign ownership from the recorded campaign coordinator. | BOUND by this card. |
| B5 | Coordination contact and recipient binding | Proposed: Codex Coordinator 2, `01a0ff59-ac63-76a1-ab49-f9cd5515ff24`, because Joshua routed the dot notice through it. The charter names "Codex coordinator" `01a0fa4b-8a76-7201-9c2f-98297042475a`, now Coordinator 1. A renamed chat is not a transfer of campaign ownership. | **MISSING — owner: coordinator (3), with Joshua if he wants Coordinator 1.** Record which chat is the dot's contact, and that Coordinator 1 keeps its existing role. |
| B6 | Recipients and access | (a) Repository: `Joshua-Asante/first-passage` (public), with push to `codex/*` branches and permission to open PRs. (b) GitHub identity the dot acts as: unknown. (c) Surface: local host or cloud, unknown. This card needs the local operations launcher (`python -I scripts/fp.py`) and the installed git hooks, so a local surface is required unless the dot shows both working elsewhere. (d) Reaching coordinator (3): through PR comments and Codex Coordinator 2 only. (e) The *Grant gap* reading of comments. | **MISSING — owner: Joshua** for (b) and (c); **coordinator (3)** for (e). |
| B7 | Card | This file, at the commit that adds it on `claude/dot-card-calendar-ratification`. That commit is the dispatch revision. | BOUND on commit; coordinator (3) records the SHA in its release record. |
| B8 | Budget and concurrency | One executor, the dot itself. No worker, subagent, scheduled task or cloud run. No new compute or spend budget: ordinary task usage within the existing allowance. CI runs only because of the dot's own pushes; `ci.dispatch` is not granted. | BOUND by this card. |
| B9 | Write footprint | Branch `codex/dot-2026-11-calendar-ratification` (new, from `main` after #622 merges). Files: `ops/calendars/RATIFIED.json`, `ops/calendars/README.md`, `tests/ops/test_book_session_calendar.py`. Disjoint from every other released card **only after #622 merges**, because #622 writes the same README and test file. | BOUND by this card; serialised behind #622 (§9 case 6). |
| B10 | Evidence destination | PR comments prefixed `[dot → coordinator (3)]`. Each carries full 40-character SHAs and, for each launcher run, the `record.json` path plus its `status`, `verification_exit_code`, `source_stable` and the test counts. The return packet (§6) is also a PR comment. | BOUND by this card. |
| B11 | Notification owner | Proposed: coordinator (3) owns every notification to Joshua for this card, including the decision packet. The dot notifies only coordinator (3), through B10 and B5. | **PROPOSED — owner: coordinator (3)** to confirm. |
| B12 | Monitor reconciliation | Coordinator 1's heartbeat covers Claude (2). No monitor covers coordinator (3). This card creates no schedule or subscription. The dot uses its own supported wake behaviour without promising timing, and coordinator (3) checks the PR when the return arrives. No existing monitor is cancelled or duplicated. | BOUND for this card. Whether (3) needs a standing monitor is outside this card (owner: coordinator (3)). |
| B13 | Surface controls | Verified on the host checkout only: `core.hooksPath` = `C:\Users\joshu\multi_firm_operations\.git\hooks` (shared by worktrees). The pre-commit gates from `scripts/install_hooks.sh` / `install_hooks.bat`, including the vendor-data integrity gate and `handoff-brief-form`, run on Claude Code commits. They are unverified on the dot's surface: the charter warns that cloud orchestration can limit local agent hooks. `scripts/guard_operator_acts.py` is a Claude Code hook and does **not** run for the dot. If the dot uses Joshua's `gh` credential, which can merge, then "no merge" holds only by instruction: the `main` ruleset requires a PR and `skills (3.12)`, but does not stop that credential from merging a green PR. | **MISSING — owners: the dot** (show its first commit's hook output in the first PR comment; `--no-verify` is forbidden), **and Joshua** (which credential the dot holds, and whether a non-merge-capable identity is used). |
| B14 | Ratification row values `RATIFIED_UTC` and `INSTRUCTION` | The loader requires `ratified_utc` ≥ the November file's `generated_utc` `2026-10-03T01:03:53Z`, and before its coverage end `2026-11-30T22:00:00Z`. Admission starts at that instant (README `:148`, loader `:599-600`). Both precedents (September `ratify calendar 650e8aab`; October, PR #560) recorded Joshua's instruction first, and the agent then wrote the row with that instant. A row written before he acts cannot honestly carry the instant of his act. Options: **(a) instruction first (recommended; matches both precedents):** Joshua says "ratify calendar b89562a5"; coordinator (3) records the UTC second and his exact words as the two values; his later merge of the clean head carries it. **(b)** Coordinator (3) already holds Joshua's 2026-10-02 sheet-2 words with a UTC timestamp ≥ `2026-10-03T01:03:53Z` that ratify this digest: use those. **(c) single touch:** `RATIFIED_UTC` = `2026-10-28T22:00:00Z` (the November coverage start, as an effective-from instant), with `INSTRUCTION` naming the go on the PR. This departs from precedent, puts agent words in the `instruction` field, and is honest only if the merge comes before that instant. | **MISSING — owner: coordinator (3)** (Joshua if (c) is chosen, since it changes the precedent). |
| B15 | Prerequisite | PR #622 (`claude/calendar-2026-11`, head `74255561f168b7bf77ca08d0fdec1eeb0cd1be6c`) is **OPEN, not merged**. Digest `b89562a58a665daa4054f310f41007f815bb45b54444c6404ad463ac0b60aad7` was recomputed from that head's `ops/calendars/book_session_calendar_2026-11.json` bytes. Relay-CLEAN is reported by the coordinator; no Codex review is visible on the PR. | **MISSING — owner: Joshua** (his go / merge of #622). |

### 0.2 Phase-0 reads (read-report-before-code)

Report these reads in the first PR comment, or before the PR exists in a `[dot → coordinator (3)]` relay through B5, before any edit. Bounce `NEEDS_CONTEXT` on any contradiction.

1. **Premise.** #622 is MERGED. Its merge commit is an ancestor of `origin/main`. On `origin/main`, `sha256(ops/calendars/book_session_calendar_2026-11.json)` = `b89562a58a665daa4054f310f41007f815bb45b54444c6404ad463ac0b60aad7` and `NOV_CALENDAR_SHA256` in the test file equals it. If either differs, the prerequisite has changed (§7).
2. **Release.** Coordinator (3)'s release record exists, cites this card's commit and gives B2, B3, B5, B6, B11, B13 and B14 values. Without it, stop.
3. **Reads.** Read these in full: `ops/calendars/RATIFIED.json`; `ops/calendars/README.md` `:145-200`; `ops/c1_rail/book_session_calendar.py` `:548-601`; and in `tests/ops/test_book_session_calendar.py`, `test_checked_in_ratification_binds_exactly_the_checked_in_bytes`, `test_october_is_ratified_and_admits`, `test_defective_ratification_files_are_refused` and the November block added by #622. Also read PR #560's diff as the precedent.
4. **Existing work.** Search GitHub for an existing branch or PR for this ratification (`gh pr list --state all --search "b89562a5"`, `git ls-remote origin 'refs/heads/codex/dot-*'`). Reuse what exists; never create a duplicate (§8).
5. **Test 0, vendor bytes and secrets.** This card reads no gitignored vendor-data path, no `.env`, no secret, no Pine and no runtime port. None is staged for this dispatch, and none is needed. Account identifiers and private figures stay out of every comment.

## 0.5. Clarifying questions and routing

- **Routing.** This is a frozen, precedented, three-file follow-through, so the worker seat suffices (routing test 2). It authors no doctrine and touches no locked or `core/` anchor surface (test 1). Ratification itself is an operator act (`governance.ratify`, `pr.merge`, both `high`), which this card leaves to Joshua.
- **Questions owed before release, not during execution:** B1, B2, B5, B6, B11, B13, B14, B15. A question that comes up during execution is returned as `NEEDS_CONTEXT`; the dot never resolves it on its own.
- **Scope note for coordinator (3).** The relayed assignment said "any other file" is out of scope. Appending the November row, however, makes #622's `test_november_is_not_ratified` fail, and `test_checked_in_ratification_binds_exactly_the_checked_in_bytes` pins the ratified set. PR #560 edited the test file for the same reason. This card therefore includes `tests/ops/test_book_session_calendar.py` in the footprint, limited to the §2 edits.

## 1. Selected outcome

A PR from `codex/dot-2026-11-calendar-ratification` against `main` appends the operator ratification row for November digest `b89562a5…` to `RATIFIED.json`. It changes the README's November row to "ratified" and records Joshua's sheet-2 acceptances, and it swaps the test's not-ratified assertion for a ratified-and-admits assertion. The PR is carried to Codex or relay CLEAN at one exact head and returned to coordinator (3) with a one-line decision packet for Joshua. The PR is not merged; ratification happens only by Joshua's act.

Joshua's sheet-2 acceptances to record, as given by the operator directly to coordinator (3) on 2026-10-02 ("all recommended" on sheet 2 item 2):
- The 2026-11-26 row's `cme_trade_date` 2026-11-26 is accepted explicitly as-is. CME puts that session in trade date 2026-11-27, and the authoring tool has no trade-date input. He accepted September's Labor Day row the same way.
- 2026-11-11 DENIED `MISSING_SOURCE` is accepted.
- 2026-11-25 and 2026-11-30 PERMITTED are accepted.
- A Thanksgiving re-check on or after 2026-11-12 is owed. A changed byte means a new digest and a new decision.

## 2. Scope (exact edits; nothing else)

1. **`ops/calendars/RATIFIED.json`:** append one object to `ratifications`, after the October row. Edit no existing row, and keep the file's existing 2-space JSON formatting and trailing newline (write LF bytes). The keys are exactly the loader's `_RATIFICATION_KEYS`:
   - `calendar_id`: `tradeify-select-100k/forward/2026-11`
   - `calendar_file`: `ops/calendars/book_session_calendar_2026-11.json`
   - `calendar_sha256`: `b89562a58a665daa4054f310f41007f815bb45b54444c6404ad463ac0b60aad7`
   - `closure_overlay_file`: `ops/calendars/book_closure_overlay.json`
   - `closure_overlay_sha256`: `483f2324b85548e60429b823454641a0ee6e34c8ef2a9cadc7dcc6555f7def5b`. Recompute it from `main` and stop if it differs.
   - `coverage_start_utc`: `2026-10-28T22:00:00Z`; `coverage_end_utc`: `2026-11-30T22:00:00Z`. Both come from the calendar's `coverage` block.
   - `ratified_by`: `operator`
   - `ratified_utc`: B14 `RATIFIED_UTC`; `instruction`: B14 `INSTRUCTION`
   - `record`: the URL of the PR this card opens
   - `scope`: "Book permission rows for the November 2026 monthly extension, including the 2026-10-29 and 2026-10-30 rollover overlap rows, as authored: 2026-11-11 DENIED (MISSING_SOURCE), 2026-11-26 DENIED (HOLIDAY), 2026-11-27 DENIED (SHORTENED); 2026-11-25 and 2026-11-30 PERMITTED accepted; the 2026-11-26 row's cme_trade_date 2026-11-26 accepted by the operator as-is (CME trade date 2026-11-27; authoring tool has no trade-date input); Thanksgiving halts provisional, re-check on or after 2026-11-12 owed and any changed byte is a new digest and a new decision. Grants no activation, deployment, resumption or historical legality."
2. **`ops/calendars/README.md`:** in the November table row added by #622 only, replace the lead "**Candidate, not ratified (digest `b89562a5…`).**" with "**Ratified by the operator (<date of `RATIFIED_UTC`>, digest `b89562a5…`).**". At the end of the row, append one sentence recording the four §1 acceptances and "Admission starts at the row's `ratified_utc`." Keep the ⚠ trade-date sentence. No other README line changes; the "Monthly extension" paragraph and December text stay as they are.
3. **`tests/ops/test_book_session_calendar.py`:**
   - In `test_checked_in_ratification_binds_exactly_the_checked_in_bytes`, change the set to `{CALENDAR_SHA256, OCT_CALENDAR_SHA256, NOV_CALENDAR_SHA256}`. The docstring sentence becomes: the October and November rows are the only other ratifications, checked in their own tests.
   - Replace `test_november_is_not_ratified` with `test_november_is_ratified_and_admits`, asserting exactly:
     - (i) the raw load `load_november().session_for(et(2026, 11, 16, 9)).refusal == "calendar_not_ratified"`;
     - (ii) the row for `NOV_CALENDAR_SHA256` has `closure_overlay_sha256 == OVERLAY_SHA256`, `ratified_by == "operator"`, `instruction == INSTRUCTION`, `ratified_utc == RATIFIED_UTC`, and coverage `("2026-10-28T22:00:00Z", "2026-11-30T22:00:00Z")`;
     - (iii) `load_ratified_calendar(NOV_CALENDAR, …)` has `calendar_digest == NOV_CALENDAR_SHA256`, and `ratified_at` equals `RATIFIED_UTC` parsed as UTC;
     - (iv) `session_for(et(2026, 11, 16, 9), expected_digest=NOV_CALENDAR_SHA256).permitted`, and the same for 2026-11-25 and 2026-11-30 at 09:00 ET;
     - (v) the refusals for 11-11, 11-26 and 11-27 at 09:00 ET are `session_denied:MISSING_SOURCE`, `session_denied:HOLIDAY` and `session_denied:SHORTENED`;
     - (vi) in the raw file, the 2026-11-26 row's `cme_trade_date` is `2026-11-26` for all four products, which pins the accepted defect so that a re-author is visible.
   - No other test changes. A further test that fails because of the appended row is a §7 stop, not a licence to edit it.

## 3. Method

Cut a worktree from `origin/main` after Phase 0. Make the §2 edits with LF bytes. Run the §4 checks through the launcher (`python -I scripts/fp.py python -m pytest tests/ops/test_book_session_calendar.py`, then `python -I scripts/fp.py check`). Run `git diff --stat`, then commit with the hooks active. Push the branch and open the PR, whose body states it is **not ratified until Joshua's act**. Request `@codex review`, or the relay review that coordinator (3) names through B5. Fix in-scope findings within §2 and re-run the affected checks. Repeat until CLEAN at one exact head, then deliver §6.

## 4. Verification (falsifier-first)

**H:** appending exactly this row, with these three file edits, makes the November digest admissible from `RATIFIED_UTC` and leaves September and October admission and every other calendar test unchanged.

**Reject if** (falsifier):
- any named acceptance test fails at the return head;
- `fp check` exits non-zero, apart from a pre-existing failure shown to fail identically on `main`, disclosed and not counted as a pass;
- the diff touches a file or line outside §2;
- an existing `RATIFIED.json` row's bytes change;
- the calendar or evidence digests differ from §0.2 item 1.

**Fail-first evidence.** On the branch before the RATIFIED row is appended, `test_november_is_ratified_and_admits` must fail with `calendar_not_ratified`, as a launcher record. After the append it must pass. A test that cannot be made to fail before the append is a §7 stop.

**Revert trigger:** any admission decision for a September or October instant differs from `main`.

Return-head evidence:
- the full `tests/ops/test_book_session_calendar.py` launcher record (expect #622's 153 plus or minus the swapped test, all passing);
- the `fp check` record;
- `git diff --check`;
- `git diff --stat origin/main...HEAD` showing exactly three files;
- `required skills (3.12)` green at the exact head.

## 5. Forbidden

- Merging, auto-merge, approving the PR, pushing to `main`, or describing the calendar as ratified anywhere except in the row the PR proposes.
- Editing `book_session_calendar_2026-11.json`, any evidence file, the overlay, the October or September files, or any existing `RATIFIED.json` row.
- Re-authoring the calendar, the Thanksgiving re-check, December authoring, or any trade-date-input build.
- `core/`, `lab/`, Pine, runtime ports, `ops/c1_rail/**` code, `scripts/**`, `.claude/**`, `AGENTS.md`, `STATE.md`, ledgers, ADRs and campaign records.
- Dispatching workers, subagents, CI workflows or cloud runs; creating schedules or monitors; any spend, arm, deploy or trade action.
- `git commit --no-verify`, `git stash`, force-push to a branch the dot did not create, and deleting any branch, PR, comment or worktree.
- Committing or quoting account identifiers, P&L, vendor CSVs, Pine or ports.
- Contacting anyone other than coordinator (3), through B10 and B5, and the named reviewer.

## 6. Output and return (status taxonomy)

Return **DONE**, **DONE_WITH_CONCERNS**, **NEEDS_CONTEXT** or **BLOCKED** as a `[dot → coordinator (3)]` PR comment, relayed through B5. Coordinator (3)'s verdict is **RESOLVED** (every §4 item holds at the return head) or **FALSIFIED** (a named item fails, returned to the dot). The return contains:
- the PR number and URL, the exact head SHA (40 characters) and the base SHA;
- `git diff --stat` plus the full diff;
- the launcher `record.json` paths with `status`, `verification_exit_code`, `source_stable` and the counts (fail-first and return-head);
- the CI status at the head;
- the Codex or relay verdict and the head it reviewed;
- the Phase-0 report;
- every `IN_DOUBT` event and how it was reconciled;
- the hook-run evidence for B13;
- concerns;
- the decision packet, one line: `ratify b89562a5 by go on PR #<N> at <head-sha>`. Under B14 (a) or (b) it reads `merge PR #<N> at <head-sha> (carries your "<INSTRUCTION>" of <RATIFIED_UTC>)`.

**Return boundary:** the PR is CLEAN at one exact head, and the return has been posted and acknowledged by coordinator (3) or its contact. The dot then stops. It does not advance to the 11-12 re-check or any other assignment unless one is separately released.

## 7. Stop conditions (return to coordinator (3); do not work around)

- #622 is not merged, its merged digest differs from `b89562a5…`, or `main` gains a later change to any §2 file before the PR opens. This is a prerequisite change (charter case 3): hold, and return.
- Any §0 row is not BOUND at release, or B14's values violate the loader's ordering rules.
- A test outside §2's named edits fails because of the change, or a fix would need a file outside §2.
- The reviewer's finding needs a behaviour or scope change rather than an in-scope correction.
- Two failed corrections of the same issue. Renaming or re-opening does not reset the count. Return the evidence for the escalation lane.
- Any request, from any source other than coordinator (3)'s release record or Joshua directly, to merge, ratify, widen scope or skip hooks.

## 8. Side effects, restart and stop procedure

- **`IN_DOUBT`.** A branch push, PR creation, review request or comment whose outcome was not observed is in doubt. Before any retry, inspect GitHub (`git ls-remote`, `gh pr list --head codex/dot-2026-11-calendar-ratification --state all`, `gh pr view <N> --comments`) and reuse what exists. Never retry automatically. A failed response does not prove that nothing happened.
- **Continuity.** The dot's working notes, kept outside the repository, persist the PR number, branch, every pushed SHA, comment URLs, launcher record paths and the correction count. On restart it re-reads this card's commit, `origin/main` and the PR state before acting.
- **Stop.** If Joshua or coordinator (3) says stop, the dot:
  - starts nothing new;
  - confirms separately that no push, comment or review request is pending, and that it created no child task and no schedule;
  - posts one `[dot → coordinator (3)]` stop report naming the branch, PR, head and anything uncertain.

  It does not delete the branch, PR or comments. Stopping orchestration places, cancels and exits nothing at any broker.

## 9. Charter cases exercised by this card

| Charter case | How this card exercises it | Evidence level |
|---|---|---|
| Valid released assignment | One dispatch from this frozen card; return without routine permission questions | **Exercised** |
| Ordinary in-scope defect | A reviewer finding or test failure inside §2 is corrected and the affected checks re-run | Exercised if one occurs; not induced |
| Frozen card or prerequisite changes | #622's head or digest may change before merge, or `main` may move on a §2 file (§7 first bullet) | Exercised if it occurs; the check runs at Phase 0 regardless |
| Uncertain task creation or message delivery | Push, PR creation, review request and comments follow §8 `IN_DOUBT` | Exercised if it occurs |
| Restart with unfinished work | §8 continuity notes and re-inspection | Exercised only if the dot restarts mid-card; not induced |
| Concurrent assignments | The footprint collides with #622 (README, test file), so the card is **serialised** behind it, not run in parallel | **Exercised by construction** (serialise branch). The parallel branch is not exercised |
| Local computer unavailable | Launcher records need the local operations environment. If it is unavailable, mark local evidence unavailable, continue GitHub-side preparation and return `BLOCKED` or `DONE_WITH_CONCERNS`, never DONE | Exercised if it occurs |
| Worker reports success without required evidence | The dot is its own executor: no DONE without records and the exact reviewed head; a reviewer "clean" on a different head is not CLEAN | **Exercised** as a self-check at return |
| Specification conflict or repeated failed corrections | §7 stops and the two-correction rule | Exercised if it occurs |
| Stop request | §8 stop procedure | Not exercised unless a stop is issued |
| Attempt to exceed authority | The assignment ends where Joshua's acts begin (merge, ratification). The dot prepares the decision packet and defers the act | **Exercised by construction** |

Not exercised by design: routing released work to a worker (no `handoff.dispatch`), parallel allocation, schedules and subscriptions, attended-session preparation and closeout.

## 10. Audit hooks (runnable)

```bash
# Card form and authority, through the launcher. Expected: RESULT: well-formed; 0 violation(s).
python -I scripts/fp.py python scripts/check_brief.py --type handoff docs/briefs/handoffs/2026-10-02-dot-card-01-calendar-ratification.md
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-02-dot-card-01-calendar-ratification.md
# Prerequisite (Phase 0). Expected: MERGED, then the November digest.
gh pr view 622 --json state,mergeCommit -q '.state + " " + .mergeCommit.oid'
git show origin/main:ops/calendars/book_session_calendar_2026-11.json | sha256sum   # b89562a5...0aad7
git show origin/main:ops/calendars/book_closure_overlay.json | sha256sum            # 483f2324...def5b
# No duplicate work (IN_DOUBT). Expected: empty before first creation.
gh pr list --state all --search "b89562a5 in:title,body"
git ls-remote origin 'refs/heads/codex/dot-2026-11-calendar-ratification'
# Scope at return. Expected: exactly the three section-2 files; no whitespace errors.
git diff --stat origin/main...HEAD
git diff --check origin/main...HEAD
# Acceptance at the return head.
python -I scripts/fp.py python -m pytest tests/ops/test_book_session_calendar.py
python -I scripts/fp.py check
```
