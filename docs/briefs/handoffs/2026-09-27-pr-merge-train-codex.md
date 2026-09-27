# PR merge train (2026-09-27): worker card for a local Codex session

**Status:** PREPARED 2026-09-27 by the coordinator at the operator's instruction: "I want a separate local codex session to help you babysit and merge all of these prs, let's delegate some tasks to it". **Dispatched** the same day, when the operator opened a local Codex session against it. **Revised 2026-09-27** after the Codex review of `bad4d189` (the revision is listed in §7). **Dispatch pin.** The session executes the card at one immutable commit: the commit named in the operator's dispatch, or in the latest coordinator **re-anchor** comment on PR #531 that the operator has passed on. A later commit on the branch is **not in force** until it is re-anchored that way. At Phase 0 the session reports the commit it executes. If the branch head is newer than that commit, it reports the difference as `NEEDS_CONTEXT` and does not adopt the new text on its own.

**Parent:** [staged acceptance handoff set](2026-09-27-staged-acceptance-handoffs.md). That file carries no authority block, so it bounds nothing beyond this card's own seat checks.

**Seat.** Worker, routed to Codex (local) by the operator under the [surface-allocation ADR](../../adr/2026-07-14-cc-cursor-surface-allocation.md) seat table: "a Claude Code or Codex session may take a packet when the operator routes one there". The coordinator is the cloud Claude Code session on `claude/clever-wozniak-bx0u95`. It keeps acceptance, every content fix, and PR #526.

**Merging is an operator act and this card does not grant it.** `pr.merge` is risk `high` in `scripts/seat_authority.yml`, and no card can delegate it. The ADR's rule 2 ([*Decision*, "Action classes and the authority block"](../../adr/2026-07-14-cc-cursor-surface-allocation.md#decision)) reads: "a merge approves one head SHA … A change after the act is a new request." The session therefore merges a PR only when the operator approves that PR at the **exact full head SHA** the session presents in its own session (§0.5 D4).

Otherwise it records the PR as `READY_AWAITING_APPROVAL` and moves on.

```yaml authority
seat: worker
parent: docs/briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md
max_risk: medium
capabilities: [repository.read, tests.run, branch.push]
constraints:
  - no_main_write
  - no_content_edit
  - branch_update_by_merge_commit_only
  - no_force_push_rebase_or_amend
  - no_auto_merge
  - merge_only_on_operator_approval_of_exact_head_sha
  - no_automatic_retry_of_in_doubt_merge
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
  - "Every merged PR: merge method is a merge commit, and the head SHA merged equals the full SHA the operator approved and whose check runs were all completed with success, skipped or neutral"
  - "Every merged PR: at merge time no unresolved chatgpt-codex-connector review thread carries a P1 or P2 badge, no human latest review is CHANGES_REQUESTED, and the latest completed Codex review ran on the PR's last non-merge commit or later"
  - "PR #527 merges only after PR #523 is merged"
  - "No push other than a base-branch merge commit to an in-scope PR head; no PR outside §1 touched"
  - "Return table (§6) lists every in-scope PR with its final state, merge SHA or blocker"
```

## 0. Phase 0: read before acting, then report

Read these, then report in your session before any update or merge. If anything below does not match, return `NEEDS_CONTEXT` and name the difference.
- `AGENTS.md`, including *Live-execution posture* and *Public-clone posture*.
- The [surface-allocation ADR](../../adr/2026-07-14-cc-cursor-surface-allocation.md), *Action classes and the authority block*, rules 1–2.
- This card, in full, from its branch head.
- The latest coordinator comment on PR #531 (`gh pr view 531 --comments`). It carries state only and never authority.
- For each PR in §1: `gh pr view <N> --json headRefOid,mergeStateStatus,mergeable,state,reviewDecision,latestReviews`.

**Private inputs: none.** This card reads no gitignored vendor-data path, no secret file, and no private Pine source or runtime port. It sends nothing to any external service beyond the GitHub calls in §3. `gh` uses the operator's local credential, which is used but never printed or copied.

**Report:**
- the card commit being executed (dispatch pin);
- each PR's head SHA and state;
- whether `gh` is authenticated as the operator;
- the no-private-input declaration above, confirmed.

## 0.5. Frozen design decisions (constraints, not options)

- **D1. The head is re-read, never carried.** Every step that acts on a head (update, merge) uses the `headRefOid` read in the same pass. An update moves the head, so after any successful update the session returns to §3 step 1. It never uses a SHA read before the update.
- **D2. Codex coverage.** The latest completed Codex review must be on the PR's last **non-merge** commit or later. A head that differs from the reviewed commit only by merges of `main` passes. The evidence comes from the PR's **top-level** comments, not the review threads:
  - the "Codex Review Summary" comment's **Completed** row commit, or
  - a "Didn't find any major issues" comment's `Reviewed commit`.

  §3 step 4 fetches both, together with the last non-merge commit.
- **D3. Human reviews block.** A `reviewDecision` of `CHANGES_REQUESTED`, or any human (non-bot) entry in `latestReviews` whose `state` is `CHANGES_REQUESTED`, blocks the PR (§3 step 4).
- **D4. Default merge authority: per-head operator approval.** When a PR passes §3 steps 3–5, the session presents to the operator the PR number, its full 40-hex head SHA, the green check list and the Codex coverage. It merges with `--match-head-commit <that SHA>` only when the operator approves **that SHA**. Any head change voids the approval, and the session re-presents.
- **D5. (Removed 2026-09-27.)** No standing or alternative merge authority exists under this card. Under ADR rule 2, every merge needs the operator's approval of one exact head SHA that already exists (D4). An agent's report that the operator approved something is not an approval.
- **D8. IN_DOUBT merge.** If `gh pr merge` errors, times out or loses its response, the outcome is **in doubt** (ADR rule 3). The session stops acting on that PR and reconciles with `gh pr view <N> --json state,mergedAt,mergeCommit,headRefOid`:
  - merged: record `MERGED` with the merge SHA;
  - still open with the same head: record `BLOCKED` (`in-doubt merge, not merged`) and report it.

  It **never retries automatically**. A retry is a new D4 approval of the then-current head. No other PR is updated or merged until the reconciliation is recorded.
- **D6. Order.** #523 merges before #527, and #531 merges last. Otherwise the first PR to go clean merges first.
- **D7. Everything is fresh at merge.** `--match-head-commit` checks only the head SHA, not checks or reviews. So immediately before merging, **after** any wait for CI or for operator approval, the session re-fetches the head, the checks, the human reviews, the Codex threads and the Codex coverage (§3 steps 1, 3 and 4). It merges only if all still pass on the same head.

## 1. Outcome and return boundary

**Outcome:** each in-scope PR ends in one of three states:
- `MERGED`, by merge commit under D4;
- `READY_AWAITING_APPROVAL`: it passes every §3 check at a named head, but the operator has not approved that head;
- `BLOCKED`, with its blocker named.

The return is the §6 table, reported to the operator in the session.

| PR | Branch | Notes |
|---|---|---|
| [#523](https://github.com/Joshua-Asante/first-passage/pull/523) | `claude/clever-wozniak-bx0u95` | Coordinator's branch, still receiving coordinator content commits. D2 applies to the latest of them. Merges before #527. |
| [#527](https://github.com/Joshua-Asante/first-passage/pull/527) | `claude/h1c-apply-build-entry` | Merges **only after #523** (it relies on the CP-1a ledger entry #523 carries). |
| [#522](https://github.com/Joshua-Asante/first-passage/pull/522) | `claude/h4-fence-classification` | Code PR. Full CI, including `Qualification S2 supervision` and `qualification-windows`. |
| [#529](https://github.com/Joshua-Asante/first-passage/pull/529) | `claude/kind-goldberg-9kzetq` | Code PR. Full CI, including `qualification-windows`. |
| This card's PR, [#531](https://github.com/Joshua-Asante/first-passage/pull/531) | `claude/pr-merge-train-codex-card` | Docs only. Merges last. |

#525 is done (merged at `ed3e476f`). **Out of scope:** #526, which the coordinator is iterating and the operator merges, and every other PR.

## 2. Division of labour

- **Codex session (this card):** keeps in-scope branches up to date with `main`, watches CI, Codex and review state, presents ready heads to the operator, merges under D4, and reports.
- **Coordinator:** every content change, every reply on a review thread, every "@codex review" request, every red-CI root cause and every merge conflict. While this card is active the coordinator does not update or merge in-scope PRs, so the two sessions never race on a head.
- A PR the session cannot advance is **left alone** and listed as blocked in §6. The coordinator receives the same GitHub events.

## 3. Loop (repeat until every in-scope PR is `MERGED`, `READY_AWAITING_APPROVAL` or `BLOCKED`)

Repository: `Joshua-Asante/first-passage`. `main` requires a PR, the `skills (3.12)` status and a branch that is up to date with `main` (strict), so every merge puts every other PR behind. Poll no more often than every 5 minutes. `pytest (3.11)` takes about 50 minutes, and `qualification-windows` can take longer.

1. **Read state:** `gh pr view <N> --json headRefOid,mergeStateStatus,mergeable,state,reviewDecision,latestReviews`.
2. **Behind `main`:** update the branch by merge commit, pinned to the head just read:
   `gh api -X PUT repos/Joshua-Asante/first-passage/pulls/<N>/update-branch -f expected_head_sha=<headRefOid>`.
   - On success the head has changed. **Go back to step 1** (D1).
   - A 422 means the head moved; go back to step 1.
   - A merge conflict is a blocker (§5 list).
3. **CI:** `gh pr checks <N>`. Wait while anything is pending or queued. Clean means every check run on the current head completed as `pass` or `skipping`. `fail` or `cancelled` is a blocker; do not re-run it.
4. **Reviews:**
   - **Human reviews (D3):** from step 1's `reviewDecision` and `latestReviews`.
   - **Codex threads:** no unresolved thread whose first comment is from `chatgpt-codex-connector` and carries a P1 or P2 badge. Read every page of threads:
     ```
     gh api graphql -f owner=Joshua-Asante -f repo=first-passage -F n=<N> -f query='
       query($owner:String!,$repo:String!,$n:Int!,$after:String){
         repository(owner:$owner,name:$repo){ pullRequest(number:$n){
           reviewThreads(first:100, after:$after){
             pageInfo{ hasNextPage endCursor }
             nodes{ isResolved comments(first:1){ nodes{ author{login} body } } } } } } }'
     ```
     While `hasNextPage` is true, repeat with `-f after=<endCursor>`.
   - **Codex coverage (D2).** Fetch the last non-merge commit and the top-level comments:
     ```
     gh api repos/Joshua-Asante/first-passage/pulls/<N>/commits --paginate \
       --jq '.[] | select(.parents | length == 1) | .sha' | tail -n 1     # PowerShell: | Select-Object -Last 1
     gh api repos/Joshua-Asante/first-passage/issues/<N>/comments --paginate \
       --jq '.[] | select(.user.login == "chatgpt-codex-connector[bot]") | {updated_at, body}'
     ```
     Take the newest "Didn't find any major issues" comment's `Reviewed commit`, or the summary comment's **Completed** row commit. The last non-merge commit must be that commit or one of its ancestors: `gh api repos/Joshua-Asante/first-passage/compare/<last-non-merge>...<reviewed>` returns `status` `identical` or `ahead`. A summary row still **Running** is not coverage.
5. **Order (D6).**
6. **Present, re-check, merge (D4, D7).**
   - Under D4: present the PR, its full head SHA, the checks and the coverage to the operator, and wait for approval of that SHA. If there is no approval, record the PR as `READY_AWAITING_APPROVAL` and move on.
   - After approval, and immediately before merging, repeat steps 1, 3 and 4 on the current head. If the head differs from the approved SHA, the approval is void: go back to step 1. If any check or review no longer passes, the PR is blocked.
   - Then run `gh pr merge <N> --merge --match-head-commit <approved SHA>`. Never squash or rebase: cited SHAs must stay reachable. Never enable auto-merge. If the result is not a clear success or refusal, apply D8.
7. After each merge, go back to step 1 for every remaining PR. You may update every remaining ready PR at once (step 2) so their CI runs in parallel.

## 4. Verification (falsifier-first)

**H:** the train merges exactly the in-scope PRs whose approved head was green, Codex-covered and free of blocking reviews, in the §0.5 D6 order, and nothing else. **Reject if** any item below is falsified; **accept if** all hold for every merge in the §6 table.
- **Head binding.** For each merge, the merged head equals the full head SHA the operator approved (D4) and the head whose checks and reviews were read. *Falsified by* any merge of a head read before an update, a merge without approval of that exact SHA, or an automatic retry after an in-doubt merge.
- **Green.** Every check run on the merged head completed as `pass` or `skipping`. *Falsified by* a merge with a pending, failed or cancelled check.
- **Reviews.** Read after the last wait (D7): no unresolved Codex P1/P2 thread on any page; Codex coverage per D2; no human `CHANGES_REQUESTED`. *Falsified by* any of these present at merge time, or by review state read only before a CI or approval wait.
- **Scope.** Only §1 PRs were updated or merged, and only by base-branch merge commits. *Falsified by* any other push, edit, comment or merge.

## 5. Forbidden

- Merging without operator approval of the exact head SHA (D4); retrying an in-doubt merge automatically (D8); enabling auto-merge; squash or rebase merges.
- Any content edit, comment, review reply, thread resolution, review request, CI dispatch or re-run.
- Force-push, rebase or amend on any branch; any push to `main`.
- Touching any PR outside §1, including #526.
- Trades, spend, deploys, arming, vendor or broker contact, and reading or quoting private Pine or runtime-port sources.

Blockers, where the session leaves the PR alone and lists it in §6:
- a new unresolved Codex P1/P2 thread, or a human `CHANGES_REQUESTED` review;
- a failed or cancelled check on the current head;
- a merge conflict on update;
- `mergeable: CONFLICTING`, or `mergeStateStatus: BLOCKED` for a reason other than being behind or pending checks;
- anything that would need a forbidden action.

## 6. Return (status taxonomy)

Report to the operator in the session, in this shape:

| PR | Final state | Merge SHA | Head merged | Approval (D4 SHA) | Blocker (if any) |
|---|---|---|---|---|---|

Final state is `MERGED`, `READY_AWAITING_APPROVAL` or `BLOCKED`. For a PR that is `READY_AWAITING_APPROVAL`, the "Head merged" column gives the full head SHA that passed §3 and is awaiting approval.

- `DONE`: every in-scope PR is merged and §4 holds (RESOLVED).
- `DONE_WITH_CONCERNS`: §4 holds for every merge, and some PRs are `READY_AWAITING_APPROVAL` or `BLOCKED`, each named with its head or blocker. The no-approval path ends here.
- `NEEDS_CONTEXT`: Phase 0 found a mismatch, or an instruction conflicts with this card.
- `BLOCKED`: nothing can advance; name the blocker. If §4 was violated, the result is FALSIFIED and must be reported first.

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

## 10. Launch and audit hooks (operator, local Codex session)

Point the session at this card **at a named commit** (the dispatch pin). Tell it to run Phase 0 first and report, and to follow §3 exactly. It merges only under §0.5 D4. To dispatch a revision, the coordinator posts a re-anchor comment on #531 naming the new commit, and the operator passes it to the session.

Audit hooks, runnable at any time by the operator or the coordinator:
```bash
# card structure and authority block, through the operations launcher (AGENTS.md; on Windows use .\fp.ps1 python ...)
python -I scripts/fp.py python scripts/check_brief.py docs/briefs/handoffs/2026-09-27-pr-merge-train-codex.md
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-09-27-pr-merge-train-codex.md
# per merged PR: merged head and merge commit (compare the head with the operator-approved SHA in §6)
gh pr view <N> -R Joshua-Asante/first-passage --json mergeCommit,headRefOid,mergedAt
gh api repos/Joshua-Asante/first-passage/commits/<mergeCommit> --jq '.parents | length'   # 2 means a merge commit
```
