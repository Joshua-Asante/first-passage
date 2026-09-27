# PR merge train (2026-09-27): worker card for a local Codex session

**Status:** PREPARED 2026-09-27 by the coordinator at the operator's instruction: "I want a separate local codex session to help you babysit and merge all of these prs, let's delegate some tasks to it". **Dispatched** the same day, when the operator opened a local Codex session against it. **Revised 2026-09-27** after the Codex review of `bad4d189` (the revision is listed in §7). The card is read from its branch, `claude/pr-merge-train-codex-card`, or from `main` once its PR merges. The session re-reads it at the start of every §3 pass.

**Parent:** [staged acceptance handoff set](2026-09-27-staged-acceptance-handoffs.md). That file carries no authority block, so it bounds nothing beyond this card's own seat checks.

**Seat.** Worker, routed to Codex (local) by the operator under the [surface-allocation ADR](../../adr/2026-07-14-cc-cursor-surface-allocation.md) seat table: "a Claude Code or Codex session may take a packet when the operator routes one there". The coordinator is the cloud Claude Code session on `claude/clever-wozniak-bx0u95`. It keeps acceptance, every content fix, and PR #526.

**Merging is an operator act and this card does not grant it.** `pr.merge` is risk `high` in `scripts/seat_authority.yml`, and no card can delegate it. The ADR's rule 2 ([*Decision*, "Action classes and the authority block"](../../adr/2026-07-14-cc-cursor-surface-allocation.md#decision)) reads: "a merge approves one head SHA … A change after the act is a new request." The session therefore merges a PR only in one of two cases:
- the operator approves that PR at the **exact full head SHA** the session presents in its own session (§0.5 D4);
- the operator has recorded a different merge authority for this train, which the session then cites (§0.5 D5).

Otherwise it reports the PR as ready and stops.

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
  - "Every merged PR: merge method is a merge commit, and the head SHA merged equals the SHA the operator approved and whose check runs were all completed with success, skipped or neutral"
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

**Report:** each PR's head SHA and state; whether `gh` is authenticated as the operator; and which merge authority applies (D4 or D5).

## 0.5. Frozen design decisions (constraints, not options)

- **D1. The head is re-read, never carried.** Every step that acts on a head (update, merge) uses the `headRefOid` read in the same pass. An update moves the head, so after any successful update the session returns to §3 step 1. It never uses a SHA read before the update.
- **D2. Codex coverage.** The latest completed Codex review must be on the PR's last **non-merge** commit or later. That review is either the "Codex Review Summary" comment's commit or a "Didn't find any major issues" comment's reviewed commit. A head that differs from the reviewed commit only by merges of `main` passes.
- **D3. Human reviews block.** A `reviewDecision` of `CHANGES_REQUESTED`, or any human (non-bot) entry in `latestReviews` whose `state` is `CHANGES_REQUESTED`, blocks the PR (§3 step 4).
- **D4. Default merge authority: per-head operator approval.** When a PR passes §3 steps 3–5, the session presents to the operator the PR number, its full 40-hex head SHA, the green check list and the Codex coverage. It merges with `--match-head-commit <that SHA>` only when the operator approves **that SHA**. Any head change voids the approval, and the session re-presents.
- **D5. Alternative merge authority.** This applies only if the operator records, in a durable place the coordinator can cite, a merge authority that covers the heads this train produces. The session then cites that record in its report and merges under it. Without such a record, D4 applies. An agent's report that the operator approved something is not an approval.
- **D6. Order.** #523 merges before #527, and #531 merges last. Otherwise the first PR to go clean merges first.

## 1. Outcome and return boundary

**Outcome:** each in-scope PR ends either merged by merge commit under D4 or D5, or blocked with its blocker named. The return is the §6 table, reported to the operator in the session.

| PR | Branch | Notes |
|---|---|---|
| [#523](https://github.com/Joshua-Asante/first-passage/pull/523) | `claude/clever-wozniak-bx0u95` | Coordinator's branch, still receiving coordinator content commits. D2 applies to the latest of them. Merges before #527. |
| [#527](https://github.com/Joshua-Asante/first-passage/pull/527) | `claude/h1c-apply-build-entry` | Merges **only after #523** (it relies on the CP-1a ledger entry #523 carries). |
| [#522](https://github.com/Joshua-Asante/first-passage/pull/522) | `claude/h4-fence-classification` | Code PR. Full CI, including `Qualification S2 supervision` and `qualification-windows`. |
| [#529](https://github.com/Joshua-Asante/first-passage/pull/529) | `claude/kind-goldberg-9kzetq` | Code PR. Full CI, including `qualification-windows`. |
| This card's PR, [#531](https://github.com/Joshua-Asante/first-passage/pull/531) | `claude/pr-merge-train-codex-card` | Docs only. Merges last. |

#525 is done (merged at `ed3e476f`). **Out of scope:** #526, which the coordinator is iterating and the operator merges, and every other PR.

## 2. Division of labour

- **Codex session (this card):** keeps in-scope branches up to date with `main`, watches CI, Codex and review state, presents ready heads to the operator, merges under D4 or D5, and reports.
- **Coordinator:** every content change, every reply on a review thread, every "@codex review" request, every red-CI root cause and every merge conflict. While this card is active the coordinator does not update or merge in-scope PRs, so the two sessions never race on a head.
- A PR the session cannot advance is **left alone** and listed as blocked in §6. The coordinator receives the same GitHub events.

## 3. Loop (repeat until every in-scope PR is merged or blocked)

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
   - **Codex coverage (D2).**
5. **Order (D6).**
6. **Re-read, present, merge.**
   - Re-read `headRefOid`. If it differs from the head checked in steps 3–4, go back to step 1.
   - Under D4: present the PR, its full head SHA, the checks and the coverage to the operator, and wait for approval of that SHA.
   - Then run `gh pr merge <N> --merge --match-head-commit <that SHA>`. Never squash or rebase: cited SHAs must stay reachable. Never enable auto-merge.
7. After each merge, go back to step 1 for every remaining PR. You may update every remaining ready PR at once (step 2) so their CI runs in parallel.

## 4. Verification (falsifier-first)

**H:** the train merges exactly the in-scope PRs whose approved head was green, Codex-covered and free of blocking reviews, in the §0.5 D6 order, and nothing else. **Reject if** any item below is falsified; **accept if** all hold for every merge in the §6 table.
- **Head binding.** For each merge, the merged head equals the head the operator approved (D4) or that the cited record covers (D5), and equals the head whose checks and reviews were read. *Falsified by* any merge of a head read before an update, or a merge without approval of that exact SHA.
- **Green.** Every check run on the merged head completed as `pass` or `skipping`. *Falsified by* a merge with a pending, failed or cancelled check.
- **Reviews.** At merge: no unresolved Codex P1/P2 thread on any page; Codex coverage per D2; no human `CHANGES_REQUESTED`. *Falsified by* any of these present at merge time.
- **Scope.** Only §1 PRs were updated or merged, and only by base-branch merge commits. *Falsified by* any other push, edit, comment or merge.

## 5. Forbidden

- Merging without operator approval of the exact head SHA (D4) or a cited durable record (D5); enabling auto-merge; squash or rebase merges.
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

| PR | Final state | Merge SHA | Head merged | Approval (D4 SHA or D5 record) | Blocker (if any) |
|---|---|---|---|---|---|

- `DONE`: every in-scope PR is merged and §4 holds (RESOLVED).
- `DONE_WITH_CONCERNS`: §4 holds for every merge, and some PRs are blocked, each named.
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

## 10. Launch and audit hooks (operator, local Codex session)

Point the session at this card on branch `claude/pr-merge-train-codex-card`. Tell it to run Phase 0 first and report, and to follow §3 exactly. It merges only under §0.5 D4 or D5.

Audit hooks, runnable at any time by the operator or the coordinator:
```bash
# card structure and authority block
python3 scripts/check_brief.py docs/briefs/handoffs/2026-09-27-pr-merge-train-codex.md
python3 scripts/check_handoff_authority.py docs/briefs/handoffs/2026-09-27-pr-merge-train-codex.md
# per merged PR: merge method and merged head (compare with the operator-approved SHA in §6)
gh pr view <N> -R Joshua-Asante/first-passage --json mergeCommit,headRefOid,mergedAt
git show --no-patch --format='%H %P' <mergeCommit>   # two parents means a merge commit
```
