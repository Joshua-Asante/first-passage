# PR merge train (2026-09-27): worker card for a local Codex session

**Status:** PREPARED 2026-09-27 by the coordinator at the operator's instruction: "I want a separate local codex session to help you babysit and merge all of these prs, let's delegate some tasks to it". **Dispatched** the same day, when the operator opened a local Codex session against it. **Revised 2026-09-27** after the Codex review of `bad4d189` (the revision is listed in §7). **Dispatch pin.** The session executes the card at one immutable commit: the commit named in the operator's dispatch, or in the latest coordinator **re-anchor** comment on PR #531 that the operator has passed on. A later commit on the branch is **not in force** until it is re-anchored that way. At Phase 0 the session reports the commit it executes. If the branch carries a **non-merge** commit after that commit, it reports the difference as `NEEDS_CONTEXT` and does not adopt the new text on its own. A merge of `main` into this branch (its own `update-branch`) does not change the card and is not newer text. **Sixth revision (2026-09-27):** the session issues no merges. The operator ruled that the train uses D4. The session then reported that its harness approves commands automatically, so it cannot guarantee an approval prompt at the moment of action, and it stopped merging. This card now matches that state: the session reports ready heads, and the operator merges.

**Parent:** [staged acceptance handoff set](2026-09-27-staged-acceptance-handoffs.md). That file carries no authority block, so it bounds nothing beyond this card's own seat checks.

**Seat.** Worker, routed to Codex (local) by the operator under the [surface-allocation ADR](../../adr/2026-07-14-cc-cursor-surface-allocation.md) seat table: "a Claude Code or Codex session may take a packet when the operator routes one there". The coordinator is the cloud Claude Code session on `claude/clever-wozniak-bx0u95`. It keeps acceptance, every content fix, and PR #526.

**Merging is an operator act, and the session does not merge.** `pr.merge` is risk `high` in `scripts/seat_authority.yml`, and no card can delegate it. The ADR's rule 2 ([*Decision*, "Action classes and the authority block"](../../adr/2026-07-14-cc-cursor-surface-allocation.md#decision)) reads: "a merge approves one head SHA … A change after the act is a new request." The operator ruled on 2026-09-27 that the train uses the card's approval step (D4). The session cannot guarantee an action-time approval prompt, so under D4 it issues no merge. It reports each ready head as `READY_AWAITING_APPROVAL` with its full SHA, and the operator merges (§0.5 D4).

**Operator ruling 2026-09-27: merge-speed process changes 1–3.** The operator ruled: "process changes 1, 2 and 3 are good, let's start them right away". The three changes are:
1. code-free PRs block on unresolved Codex P1 threads only;
2. CI results are reused across a conflict-free update from `main`;
3. code-free PRs merge first and code PRs last.

§0.5 D9–D11 are the card text for these. They change no test, skip nothing, leave the `main` ruleset (strict up-to-date plus `skills (3.12)`) unchanged, and grant no merge authority: the operator performs every merge (D4).

```yaml authority
seat: worker
parent: docs/briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md
max_risk: medium
capabilities: [repository.read, tests.run, branch.push]
constraints:
  - no_direct_push_to_main
  - no_content_edit
  - branch_update_by_merge_commit_only
  - no_force_push_rebase_or_amend
  - no_merge_by_session
  - no_auto_merge
  - no_ci_dispatch_or_rerun
  - no_pr_comment_or_thread_resolution
  - no_pr_outside_scope
  - no_rail_deploy
  - no_rail_arm
  - no_account_traffic
  - no_broker_or_vendor_contact
  - no_private_source_read
  - no_external_send
acceptance:
  - "The session ran no merge: no gh pr merge, merge API call or auto-merge. Every MERGED row is an operator merge, with the merge SHA read from GitHub after the merge"
  - "Every READY_AWAITING_APPROVAL report names a full head SHA at which, read after the last wait: every expected check run completed with success, skipped or neutral (under D10, only push-to-main workflow runs may still be pending); no unresolved chatgpt-codex-connector thread carries a P0 or P1 badge, nor on a code PR a P2 badge (D9); no human latest review is CHANGES_REQUESTED; Codex coverage holds per D2; and the D6 order and D13 backstop allow it"
  - "PR #527 is reported ready only after PR #523 is MERGED; PR #531 only after every other in-scope PR is MERGED or BLOCKED"
  - "No push other than a base-branch merge commit to an in-scope PR head; no PR outside §1 touched"
  - "Return table (§6) lists every in-scope PR with its final state, ready head or merge SHA, or blocker"
```

## 0. Phase 0: read before acting, then report

Read these, then report in your session before any update. If anything below does not match, return `NEEDS_CONTEXT` and name the difference.
- `AGENTS.md`, including *Live-execution posture* and *Public-clone posture*.
- The [surface-allocation ADR](../../adr/2026-07-14-cc-cursor-surface-allocation.md), *Action classes and the authority block*, rules 1–3.
- This card, in full, **at the pinned commit** (`git show <pin>:docs/briefs/handoffs/2026-09-27-pr-merge-train-codex.md`).
- The latest coordinator comment on PR #531 (`gh pr view 531 -R Joshua-Asante/first-passage --comments`). It carries state only and never authority.
- For each PR in §1: `gh pr view <N> -R Joshua-Asante/first-passage --json headRefOid,mergeStateStatus,mergeable,state,isDraft,reviewDecision,latestReviews`.

**Private inputs.**
- **One credential:** the operator-held `gh` credential in the operator's local environment. `gh auth status` must show the operator's GitHub account. `gh api repos/Joshua-Asante/first-passage --jq .permissions.push` must print `true`, since `gh auth status` alone does not show repository permissions. The credential is used by the §3 calls, and is never printed, copied or passed to another tool. If it is absent, belongs to another account or lacks push access, return `NEEDS_CONTEXT`.
- **No data inputs:** no gitignored vendor-data path, no secret file, and no private Pine source or runtime port.
- **Nothing sent** to any service except the GitHub calls in §3.

**Report:**
- the card commit being executed (dispatch pin);
- each PR's head SHA and state;
- whether `gh` is authenticated as the operator with push access;
- a confirmation that the session will issue no merge (D4);
- the private-input declaration above, confirmed (the `gh auth status` account).

## 0.5. Frozen design decisions (constraints, not options)

- **D1. The head is re-read, never carried.** Every step that acts on a head (update, ready report) uses the `headRefOid` read in the same pass. An update moves the head, so after any successful update the session returns to §3 step 1. It never uses a SHA read before the update.
- **D2. Codex coverage.** The latest completed Codex review must cover every commit of the PR's own history except merges that GitHub's `update-branch` made. Every PR commit after the reviewed commit must be a merge commit committed by `web-flow`, which is GitHub's `update-branch`. A non-merge commit, or a merge made anywhere else (including a coordinator's conflict-resolving merge), leaves coverage absent until Codex reviews a head at or after it. The reviewed commit comes from the PR's **top-level** comments, not the review threads:
  - the "Codex Review Summary" comment's **Completed** row commit, or
  - a "Didn't find any major issues" comment's `Reviewed commit`.

  §3 step 4 fetches it and runs the check.
- **D3. Human reviews block.** A `reviewDecision` of `CHANGES_REQUESTED`, or any human (non-bot) entry in `latestReviews` whose `state` is `CHANGES_REQUESTED`, blocks the PR (§3 step 4).
- **D4. Merge authority: the operator merges.** When a PR passes §3 steps 1–5 on a fresh read (D7), the session reports it to the operator as `READY_AWAITING_APPROVAL`. The report gives the PR number, its full 40-hex head SHA, the check list, the Codex coverage and any deferred P2s. The session issues **no merge**. The operator merges, if they choose, with `gh pr merge <N> -R Joshua-Asante/first-passage --merge --match-head-commit <that SHA>` or the web UI. `--match-head-commit` binds only the head, so the operator re-checks reviews at that moment. A ready report is a snapshot. If the head moves or a gate stops passing, the session withdraws it (D7).
- **D5. (Removed 2026-09-27.)** No standing or alternative merge authority exists under this card. Under ADR rule 2, every merge needs the operator's approval of one exact head SHA that already exists (D4). An agent's report that the operator approved something is not an approval.
- **D6. Order (ruling item 3).** When several PRs are ready, the session reports code-free PRs first (#523, then #527), then code PRs, so the slow code-PR CI reruns after as few merges as possible. That is a preference. Three hard dependencies follow (§3 step 5):
  - **#527 after #523:** #527 is reported ready only once #523 is `MERGED`. If #523 ends `READY_AWAITING_APPROVAL` or `BLOCKED`, #527 is `BLOCKED` (`order: #523 not merged`).
  - **#532 after #523 and #527:** #532 is reported ready only once both are `MERGED` or `BLOCKED` (the operator's instruction to the session).
  - **#531 last:** #531 is reported ready only once every other in-scope PR is `MERGED` or `BLOCKED`. While any other PR is `READY_AWAITING_APPROVAL`, #531 is `BLOCKED` (`order: <N> awaiting approval`).
- **D7. Everything is fresh at the ready report.** Immediately before reporting a PR ready, and after any wait, the session re-runs §3 steps 1–4 on the current head, including step 2's behind-`main` check. While a PR stays `READY_AWAITING_APPROVAL`, the session repeats those reads on every poll. If the head moves, the PR falls behind `main`, or any gate stops passing, it withdraws the ready report and says why.
- **D8. Merges are observed, not made.** Step 1 records a PR it reads as `MERGED` from that read's `mergeCommit`, which exists only after the merge: `MERGED (operator)` with the merge SHA. A PR merged before this revision is `MERGED (before re-anchor)`. Any merge moves `main`, so D13 applies before another PR is reported ready under D10.
- **D9. Code-free PRs block on P1 only (ruling item 1).**
  - **Code-free PR:** one that changes no file under `ops/`, `core/`, `lab/`, `scripts/`, `tests/`, `tools/`, `deploy/` or `.github/`, and no `*.py`, `*.ps1`, `*.sh`, `*.yml` or `*.toml` file. Documentation and pin registries such as `docs/evidence/*.sha256` qualify. Check with `gh pr diff <N> -R Joshua-Asante/first-passage --name-only`. In this train, #523, #527 and #531 are code-free; #529 and #532 are code PRs, and #522 was one.
  - On a code-free PR, only an unresolved Codex **P0 or P1** thread blocks. An unresolved Codex **P2** thread does not block. The coordinator tracks it as a follow-up, and the §6 row lists it.
  - On a code PR, P0, P1 and P2 all block, as before.
  - Human `CHANGES_REQUESTED` (D3) and Codex coverage (D2) apply to both kinds.
- **D10. CI reused across a conflict-free update from `main` (ruling item 2).** This applies to a code PR whose full CI passed at head `H0` and whose current head `H1` differs from `H0` only by a merge commit of `main`. Confirm that `gh api repos/Joshua-Asante/first-passage/commits/<H1> --jq '[.parents[].sha]'` returns exactly `[H0, <a commit on main>]`, and that the update did not report a conflict. `H0`'s results are read by SHA, never through `gh pr checks`, which shows only the current head (§3 step 3's command with `<H0>`). For such a PR, "CI clean" at `H1` means all of the following:
  - every check run on `H0` completed with `success`, `skipped` or `neutral`, and the §3 step 3 expected set was present on `H0`;
  - `skills (3.12)` completed with `success` on `H1`;
  - every check run on `H1` from a workflow that does **not** run on push to `main` has completed with `success`, `skipped` or `neutral` on `H1`. These are `qualification-windows`, `Qualification S2 supervision`, `Qualification execution boundary (…)` and any third-party check. Nothing after the merge would catch a failure of theirs;
  - no check run on `H1` has failed or been cancelled.

  Only check runs of push-to-`main` workflows (`Tests`, `Pylint`, `Gate manifest`, `Manifest check`, `Validation controls`, `c1 image validation`) may still be pending on `H1`. Record `H0` and the reuse in the §6 row. The backstop for those pending runs is `main`'s own post-merge CI, since those workflows run on every push to `main`. D13 reads that backstop before any further D10 ready report. D10 never applies to a head with any non-merge commit after `H0`. Code-free PRs keep the full step 3 rule.
- **D11. What the ruling does not change.** No test, check or gate is skipped, disabled, re-run or relaxed. The `main` ruleset is unchanged. D1–D4 and D7 all still apply.
- **D12. Waiting is bounded.** A PR that has waited more than **3 hours** on one head is recorded `BLOCKED` with the head. The wait can be for CI, Codex coverage, an order dependency, GitHub's mergeability computation or the D13 backstop. The reason is `ci-pending`, `codex-coverage-absent`, `order: <N> not merged`, `mergeability-unknown` or `backstop-pending`. A PR recorded `BLOCKED` this way is not re-evaluated in the same run. A new dispatch or re-anchor starts it again.
- **D13. The post-merge backstop is read before further D10 reuse.** After any merge moves `main`, the session reads the new `main` commit's check runs with step 3's command. It reads them for the push-to-`main` workflows (`Tests`, `Pylint`, `Gate manifest`, `Manifest check`, `Validation controls`, `c1 image validation`, whichever ran).
  - Until they have all completed with `success`, `skipped` or `neutral`, no PR is reported ready under D10 reuse. PRs with full green CI on their own head may still be reported.
  - A failed run is reported to the coordinator at once, and D10 reuse stays suspended until the coordinator records its triage on #531.

## 1. Outcome and return boundary

**Outcome:** each in-scope PR ends in one of three states:
- `MERGED`, by the operator's merge commit (D4, D8);
- `READY_AWAITING_APPROVAL`: it passes every §3 check at a named full head SHA, and the operator has not merged it;
- `BLOCKED`, with its blocker named.

The return is the §6 table. The session reports it to the operator in the session, and the operator passes it to the coordinator, who records it on #531 and in the owning H-row. That is the committed return. A PR that is `CLOSED` without merging is `BLOCKED` (`closed externally`). A draft PR is `BLOCKED` (`draft`).

| PR | Branch | Notes |
|---|---|---|
| [#523](https://github.com/Joshua-Asante/first-passage/pull/523) | `claude/clever-wozniak-bx0u95` | Coordinator's branch, still receiving coordinator content commits. D2 applies to the latest of them. Merges before #527. |
| [#527](https://github.com/Joshua-Asante/first-passage/pull/527) | `claude/h1c-apply-build-entry` | Merges **only after #523** (it relies on the CP-1a ledger entry #523 carries). |
| [#522](https://github.com/Joshua-Asante/first-passage/pull/522) | `claude/h4-fence-classification` | Code PR. **Merged** at `38e62eed` before this revision; record it as `MERGED (before re-anchor)`. |
| [#529](https://github.com/Joshua-Asante/first-passage/pull/529) | `claude/kind-goldberg-9kzetq` | Code PR. Full CI, including `qualification-windows`. |
| [#532](https://github.com/Joshua-Asante/first-passage/pull/532) | `claude/stoic-ritchie-xcikuz` | Code PR, added by the operator's direct instruction to the session (2026-09-27). The helper Claude session owns its content and reviews. Reported ready only after #523 and #527 are `MERGED` or `BLOCKED`, and before #531. |
| This card's PR, [#531](https://github.com/Joshua-Asante/first-passage/pull/531) | `claude/pr-merge-train-codex-card` | Docs only. Merges last. |

#525 (`ed3e476f`) and #522 (`38e62eed`) merged before this revision. **Out of scope:** #526 and #533, which the coordinator drives and the operator merges, and every other PR.

## 2. Division of labour

- **Codex session (this card):** keeps in-scope branches up to date with `main`, watches CI, Codex and review state, reports ready heads to the operator (D4), and returns the §6 table. It never merges.
- **Operator:** merges ready heads.
- **Coordinator:** every content change on #523 and #531 (the helper session owns #532's), every reply on a review thread, every "@codex review" request, every red-CI root cause and every merge conflict. The coordinator still pushes content to #523 while the card is active, so a push can race the session's `update-branch`. The coordinator therefore always fetches and merges the remote head before pushing, and never force-pushes an in-scope branch. The session's D1 re-read and `expected_head_sha` pin cover its side, and a `diverged` compare in step 4 means coverage is absent.
- A PR the session cannot advance is **left alone** and listed as blocked in §6. The coordinator receives the same GitHub events.

## 3. Loop (repeat until every in-scope PR is `MERGED` or `BLOCKED`, or is `READY_AWAITING_APPROVAL` with no gate left to re-check)

Repository: `Joshua-Asante/first-passage`. `main` requires a PR, the `skills (3.12)` status and a branch that is up to date with `main` (strict), so every merge puts every other PR behind. Poll no more often than every 5 minutes. `pytest (3.11)` takes about 50 minutes, and `qualification-windows` can take longer.

1. **Read state:** `gh pr view <N> -R Joshua-Asante/first-passage --json headRefOid,mergeStateStatus,mergeable,state,isDraft,reviewDecision,latestReviews,mergeCommit`.
   - `MERGED`: record it per D8 and apply D13. `CLOSED` or a draft: record it per §1 and stop acting on the PR.
   - `mergeable` or `mergeStateStatus` `UNKNOWN`: GitHub is still computing. Re-read on the next poll, within D12.
2. **Behind `main`:** update the branch by merge commit, pinned to the head just read:
   `gh api -X PUT repos/Joshua-Asante/first-passage/pulls/<N>/update-branch -f expected_head_sha=<headRefOid>`.
   - **Before updating**, record the current head as `H0` and read its check runs by SHA (step 3's command with `<H0>`). D10 can only reuse results read here.
   - The endpoint answers **202 Accepted** and merges asynchronously. Re-read step 1 until `headRefOid` differs from `H0`, then **go back to step 1** (D1). If the head has not moved within 10 minutes, the PR is `BLOCKED` (`update did not land`).
   - On a 422, read the response `message` before doing anything else:
     - if it reports that the expected head SHA did not match, the head moved: go back to step 1;
     - if it reports a merge conflict, the PR is `BLOCKED` (`update conflict`);
     - any other message makes the PR `BLOCKED` (`update refused: <message>`).

     Never repeat the same PUT without re-reading the head first.
3. **CI, read by SHA:** `gh api repos/Joshua-Asante/first-passage/commits/<head>/check-runs --paginate --jq '.check_runs[] | [.name, .status, .conclusion] | @tsv'`.
   - **Expected set.** It must be present before "clean" is judged, so that checks not yet registered after an update are not missed.
     - The set is every job of every workflow whose `pull_request` trigger matches the PR's changed files, taken from `gh pr diff <N> -R Joshua-Asante/first-passage --name-only` against the `paths` and `paths-ignore` filters in the head's `.github/workflows/*.yml`.
     - It always includes `skills (3.12)` and both `Qualification execution boundary` jobs.
     - It includes the PR-only `qualification-windows` and `Qualification S2 supervision` jobs whenever their filters match.
     - A job in the set that is missing from the head's check runs is pending.
   - **Clean:** every check run on the head has status `completed` with conclusion `success`, `skipped` or `neutral`. The one exception is D10, for a code PR whose only change is a merge of `main`.
   - **Blocker:** `failure`, `cancelled`, `timed_out`, `action_required`, `startup_failure` or `stale`. Do not re-run it.
   - Otherwise wait, within D12.
4. **Reviews:**
   - **Human reviews (D3):** from step 1's `reviewDecision` and `latestReviews`.
   - **Codex threads:** a code PR must have no unresolved thread whose first comment is from `chatgpt-codex-connector` and carries a P0, P1 or P2 badge. A code-free PR must have none with a P0 or P1 badge (D9). Read every page of threads:
     ```
     gh api graphql -f owner=Joshua-Asante -f repo=first-passage -F n=<N> -f query='
       query($owner:String!,$repo:String!,$n:Int!,$after:String){
         repository(owner:$owner,name:$repo){ pullRequest(number:$n){
           reviewThreads(first:100, after:$after){
             pageInfo{ hasNextPage endCursor }
             nodes{ isResolved comments(first:1){ nodes{ author{login} body } } } } } } }'
     ```
     While `hasNextPage` is true, repeat with `-f after=<endCursor>`.
   - **Codex coverage (D2).** The same commands work in bash and in PowerShell 7.3+, the launcher's baseline (AGENTS.md). Each is one line, and embedded quotes pass through natively.
     ```
     gh api repos/Joshua-Asante/first-passage/issues/<N>/comments --paginate --jq '.[] | select(.user.login == "chatgpt-codex-connector[bot]") | {updated_at, body}'
     gh api repos/Joshua-Asante/first-passage/compare/<reviewed>...<head> --jq '{status, total_commits, commits: [.commits[] | [.sha, (.parents | length), .committer.login] | @tsv]}'
     gh api repos/Joshua-Asante/first-passage/pulls/<N>/commits --paginate --jq '.[].sha'
     ```
     1. From the first command, take the newest "Didn't find any major issues" comment's `Reviewed commit`, or the summary comment's **Completed** row commit. A summary row still **Running** is not coverage.
     2. In the second command's output, `status` must be `identical` or `ahead`. A `behind` or `diverged` status means coverage is absent. If `total_commits` exceeds the commits listed, coverage is absent too, and the session asks the coordinator.
     3. Every commit it lists that is also in the third command's output (the PR's own commits, not `main`'s) must have parent count 2 and committer `web-flow`. Otherwise coverage is absent (D2).
5. **Order (D6, D13).** Apply the hard dependencies: #527 only after #523 is `MERGED`; #532 only after #523 and #527 are `MERGED` or `BLOCKED`; #531 only after every other in-scope PR is `MERGED` or `BLOCKED`. A D10-reuse report also waits for D13. Among PRs that are ready and free to go, report code-free PRs first.
6. **Report ready (D4, D7).** Immediately before reporting, and after any wait, repeat steps 1–4 on the current head. That includes step 2's behind-`main` check. Then report the PR as `READY_AWAITING_APPROVAL` with its full head SHA, the check list, the Codex coverage, any D10 `H0` and any deferred P2s. Issue no merge. Keep re-reading per D7 until the operator merges it or it stops passing.
7. When step 1 reads a merge, apply D8 and D13, then go back to step 1 for every remaining PR. You may update every remaining PR at once (step 2) so their CI runs in parallel. That can void ready reports whose heads move.

## 4. Verification (falsifier-first)

**H:** the session reports ready exactly those in-scope heads that were green, Codex-covered, free of blocking reviews and order-eligible when last read, and it merges nothing. **Reject if** any item below is falsified; **accept if** all hold for every row in the §6 table.
- **Ready binding.** Each ready report names the full head SHA whose checks and reviews were read after the last wait (D7). *Falsified by* a ready report of a head read before an update or before a wait, or a ready report left standing after its head moved.
- **No merge by the session.** *Falsified by* any `gh pr merge`, merge API call or auto-merge request made by the session. Every `MERGED` row is an operator merge (or a merge before this revision), with the merge SHA read from GitHub.
- **Green.** At each ready head, every expected check run completed with `success`, `skipped` or `neutral`. Under D10, only check runs of push-to-`main` workflows may be pending, and only with `H0` recorded, all of `H0`'s check runs green, and D13 satisfied. *Falsified by* a ready report with a failed or cancelled check, a missing expected job, or a pending check that D10 does not cover.
- **Reviews.** Read after the last wait: no unresolved Codex P0/P1 thread on any page, and on a code PR no P2 either (D9); Codex coverage per D2; no human `CHANGES_REQUESTED`. *Falsified by* any of these present at a ready report.
- **Scope.** Only §1 PRs were updated, and only by base-branch merge commits. *Falsified by* any other push, edit, comment or merge.

## 5. Forbidden

- Any merge: `gh pr merge`, the merge API, or enabling auto-merge (D4).
- Any content edit, comment, review reply, thread resolution, review request, CI dispatch or re-run.
- Force-push, rebase or amend on any branch; any push to `main`.
- Touching any PR outside §1, including #526.
- Trades, spend, deploys, arming, vendor or broker contact, and reading or quoting private Pine or runtime-port sources.

Blockers, where the session leaves the PR alone and lists it in §6:
- a new unresolved Codex P0/P1 thread, or on a code PR a P2 thread (D9), or a human `CHANGES_REQUESTED` review;
- a failed, cancelled, timed-out, startup-failed or stale check on the current head;
- a wait past the D12 bound;
- a merge conflict on update;
- `mergeable: CONFLICTING`, or `mergeStateStatus: BLOCKED` for a reason other than being behind or pending checks;
- anything that would need a forbidden action.

## 6. Return (status taxonomy)

Report to the operator in the session, in this shape:

| PR | Final state | Merge SHA (operator) | Ready head (full SHA) | D10 reuse (`H0`, or none) | Deferred P2s (D9) | Blocker (if any) |
|---|---|---|---|---|---|---|

Final state is `MERGED (operator)`, `MERGED (before re-anchor)`, `READY_AWAITING_APPROVAL` or `BLOCKED`.

- `DONE`: every in-scope PR is merged and §4 holds (RESOLVED).
- `DONE_WITH_CONCERNS`: §4 holds, and some PRs are `READY_AWAITING_APPROVAL` or `BLOCKED`, each named with its head or blocker.
- `NEEDS_CONTEXT`: Phase 0 found a mismatch, or an instruction conflicts with this card.
- `BLOCKED`: no PR merged and none is `READY_AWAITING_APPROVAL`; name every blocker. (`DONE_WITH_CONCERNS` applies when at least one PR merged or is ready.) If §4 was violated, the result is FALSIFIED and must be reported first.

## 7. Revision 2026-09-27 (Codex review of `bad4d189`)

| Finding | Change |
|---|---|
| Card did not pass `check_brief.py` | Restructured into §0–§7 and §10 |
| Stale head after `update-branch` | D1; step 2 returns to step 1; step 6 re-reads before merging |
| Human reviews not queried | D3; step 1 reads `reviewDecision` and `latestReviews` |
| Standing instruction treated as merge approval for future heads | D4 per-head approval (ADR rule 2), with D5 for a recorded alternative |
| GraphQL selected fields on a connection | Step 4 query uses `reviewThreads(first:100){ nodes … pageInfo … }` with pagination |

Second revision (Codex review of `315dfd04`):

| Finding | Change |
|---|---|
| Review state read before the CI and approval waits | D7; step 6 re-runs steps 1, 3 and 4 after approval, immediately before merging |
| No state for a ready but unapproved PR | `READY_AWAITING_APPROVAL` in §1 and §6; `DONE_WITH_CONCERNS` covers it |
| Codex coverage evidence never fetched | D2 names the top-level comments; step 4 fetches them, the last non-merge commit, and the compare |
| Audit hooks bypassed the launcher | §10 runs them through `scripts/fp.py` (or `.\fp.ps1`) |
| `git show` on a merge commit that exists only on the server | §10 reads the parents through the GitHub API |

Third revision (Codex review of `fbb1bd91`):

| Finding | Change |
|---|---|
| D5 allowed standing authority over heads not yet created | D5 removed; D4 per-head approval is the only merge path |
| Card read from a moving branch head | Dispatch pin in the Status paragraph: executes one commit; re-anchor required; a newer head is `NEEDS_CONTEXT` |
| Loop never terminates on `READY_AWAITING_APPROVAL` | §3 heading lists all three terminal states |
| No private-input declaration in Phase 0 | §0 "Private inputs: none" and report item |
| Paginated commit list gave one SHA per page | Step 4 emits every page's SHAs and takes the last line |
| No handling of an in-doubt merge | D8: reconcile through `gh pr view`, no automatic retry, train paused until recorded |

Fourth revision (operator ruling 2026-09-27 and Codex review of `7f96488e`):

| Item | Change |
|---|---|
| Operator ruling, process changes 1–3 | D9 (code-free PRs block on P1 only), D10 (CI reused across a conflict-free update from `main`, with the post-merge `main` backstop), D6 order, D11 (nothing skipped; ruleset unchanged) |
| The `gh` credential not declared as a private input | §0 names the operator-held credential and the `gh auth status` check |
| D8 did not cover a moved head, a closed PR or a failed query | D8 classifies all of them; an unresolved outcome stays IN_DOUBT and the train stays paused |
| 422 on `update-branch` retried blindly | Step 2 reads the message; only a head mismatch loops back to step 1 |
| PowerShell form was not runnable | Step 4 gives one-line bash and PowerShell forms |

Fifth revision (Codex review of `7fa16c49` and a coordinator pre-review of `7f96488e`):

| Finding | Change |
|---|---|
| Acceptance and §4 still blocked code-free PRs on P2 (Codex P1) | Acceptance, §4 and §5 carry D9 |
| Acceptance and §4 made every D10 merge a violation (Codex P1) | Acceptance and §4 carry the D10 exception |
| D10 let PR-only workflows (`qualification-windows`, S2 supervision, execution boundary) stay pending with no post-merge backstop (Codex P1) | Only push-to-`main` workflows may be pending; PR-only and third-party checks must be green on `H1` |
| `H0` results were never fetched (Codex P1) | Step 2 records `H0` and reads its check runs by SHA before updating |
| Clear merge refusals had no outcome (Codex P2) | Step 6 classifies head or base races (back to step 1) and other refusals (`BLOCKED`) |
| A chat message was the approval channel (pre-review P1) | D4: the operator approves the exact merge command at the harness prompt, or merges; no prompt means no merge |
| No wait bound or order terminal states (pre-review P1) | D12 three-hour bound; D6 and step 5 define the two hard dependencies |
| D2 accepted any merge commit (pre-review P1) | D2 accepts only `web-flow` (`update-branch`) merges after the reviewed commit |
| `update-branch` is asynchronous (202); `UNKNOWN`, closed, draft and external merges were undefined; `gh pr checks` buckets and SHA binding; `-R` missing; P0 badges; Phase 0 read the branch head; race with coordinator pushes; return not committed; §6 table columns | Step 2 polls for the new head; step 1 and §1 classify the states; step 3 reads check runs by SHA with an expected set; `-R` on every `gh pr` call; P0 blocks; Phase 0 reads the pinned commit and "newer" means a non-merge commit; §2 race rule; §1 return path; §6 columns fixed |
| `no_main_write` read as forbidding the merge itself | Renamed `no_direct_push_to_main` |

Sixth revision (operator ruling on D4, the session's report that it cannot guarantee an approval prompt, and Codex review of `ccb58135`):

| Finding | Change |
|---|---|
| The session cannot guarantee an action-time approval prompt | The session issues no merge. D4: it reports ready heads and the operator merges. `no_merge_by_session` constraint; §4 and §5 carry it |
| Harness-prompt wait skipped a final review read (Codex P1) | No session merge; the ready report is re-read every poll (D7), and the operator re-checks at merge time |
| Merge SHA read before the merge (Codex P2) | D8: merges are observed through step 1's read after the merge |
| Prompt binding falsified prior and operator merges (Codex P1) | §4 splits the ready binding from operator merges; `MERGED (before re-anchor)` and `MERGED (operator)` rows |
| An open PR after a timed-out merge was treated as settled (Codex P1) | The session makes no merge, so there is no in-doubt merge to reconcile. D8 replaced |
| Post-merge backstop never read (Codex P1) | D13: the new `main` commit's push-workflow runs gate further D10 ready reports; a failure goes to the coordinator |
| Expected set omitted PR-only jobs (Codex P1) | Step 3 derives the expected set from each workflow's `pull_request` path filters against the PR diff; execution boundary always included |
| `gh auth status` does not show repository permissions (Codex P2) | Phase 0 also checks `.permissions.push` |
| `gh pr view`/`gh pr diff` without `-R` (Codex P2) | D8's reconciliation is removed; D9's and step 3's `gh pr diff` carry `-R` |
| `UNKNOWN` mergeability unbounded (Codex P2) | D12 covers `mergeability-unknown` and `backstop-pending` |
| `startup_failure` not a blocker (Codex P2) | Step 3 and §5 list it |
| #532 added by the operator's instruction to the session | §1 row and order: after #523 and #527, before #531 |

## 10. Launch and audit hooks (operator, local Codex session)

Point the session at this card **at a named commit** (the dispatch pin). Tell it to run Phase 0 first and report, and to follow §3 exactly. It never merges (§0.5 D4). The operator merges each reported ready head at its full SHA. To dispatch a revision, the coordinator posts a re-anchor comment on #531 naming the new commit, and the operator passes it to the session.

Audit hooks, runnable at any time by the operator or the coordinator:
```bash
# card structure and authority block, through the operations launcher (AGENTS.md; on Windows use .\fp.ps1 python ...)
python -I scripts/fp.py python scripts/check_brief.py docs/briefs/handoffs/2026-09-27-pr-merge-train-codex.md
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-09-27-pr-merge-train-codex.md
# per merged PR: merged head and merge commit (compare the head with the ready head in §6)
gh pr view <N> -R Joshua-Asante/first-passage --json mergeCommit,headRefOid,mergedAt
gh api repos/Joshua-Asante/first-passage/commits/<mergeCommit> --jq '.parents | length'   # 2 means a merge commit
```
