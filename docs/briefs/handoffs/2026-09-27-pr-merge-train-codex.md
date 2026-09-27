# PR merge train (2026-09-27): worker card for a local Codex session

**Status:** PREPARED 2026-09-27 by the coordinator at the operator's instruction ("I want a separate local codex session to help you babysit and merge all of these prs, let's delegate some tasks to it"). **READY ON** the operator opening a local Codex session against this card. The card itself is read from its branch (`claude/pr-merge-train-codex-card`) or from `main` once its PR merges; it does not have to merge first.

**Parent:** [staged acceptance handoff set](2026-09-27-staged-acceptance-handoffs.md). The parent carries no authority block, so it bounds nothing beyond this card's own seat checks.

**Seat.** Worker, routed to Codex (local) by the operator under the [surface-allocation ADR](../../adr/2026-07-14-cc-cursor-surface-allocation.md) seat table ("a Claude Code or Codex session may take a packet when the operator routes one there"). The coordinator (the cloud Claude Code session on `claude/clever-wozniak-bx0u95`) keeps acceptance, every content fix, and PR #526.

**Merging is not granted by this card.** `pr.merge` is an operator act (`scripts/seat_authority.yml`, risk `high`) and no card can delegate it. The operator's standing in-session rule for these PRs is: *merge when CI is clean and there are no open P1 or P2 issues from Codex review.* The Codex session merges only if the operator gives it that instruction directly in its own session. Without it, the session stops at §3 step 6 and reports each PR as ready.

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
  - "Every merged PR: merge method is a merge commit, and the head SHA merged equals the SHA whose check runs were all completed with success, skipped or neutral"
  - "Every merged PR: at merge time no unresolved chatgpt-codex-connector review thread carries a P1 or P2 badge, and the latest completed Codex review ran on the PR's last non-merge commit or later"
  - "PR #527 merges only after PR #523 is merged"
  - "No push other than a base-branch merge commit to an in-scope PR head; no PR outside §1 touched"
  - "Return table (§5) lists every in-scope PR with its final state, merge SHA or blocker"
```

## 1. Scope

| PR | Branch | Notes |
|---|---|---|
| [#523](https://github.com/Joshua-Asante/first-passage/pull/523) | `claude/clever-wozniak-bx0u95` | Coordinator's branch. Codex clean at `52538743`; head `e3f1d7a7` adds only a merge of `main`. **Merge first**: it unblocks #527. |
| [#527](https://github.com/Joshua-Asante/first-passage/pull/527) | `claude/h1c-apply-build-entry` | Codex clean at `7b6df3fa`. **Only after #523 merges** (it relies on the CP-1a ledger entry #523 carries). |
| [#525](https://github.com/Joshua-Asante/first-passage/pull/525) | `claude/h1c-s5-owner-text-draft` | Codex clean at `e59333b0`; head `3a1e181f` adds only a merge of `main`. |
| [#522](https://github.com/Joshua-Asante/first-passage/pull/522) | `claude/h4-fence-classification` | Code PR; no Codex threads. Full CI, including `Qualification S2 supervision` and `qualification-windows`. |
| [#529](https://github.com/Joshua-Asante/first-passage/pull/529) | `claude/kind-goldberg-9kzetq` | Code PR; Codex clean. Full CI, including `qualification-windows`. |
| This card's PR | `claude/pr-merge-train-codex-card` | Docs only. Merge last. |

**Out of scope:** [#526](https://github.com/Joshua-Asante/first-passage/pull/526). A coordinator subagent is pushing Codex fixes to it; the coordinator merges it. Every other PR is out of scope.

## 2. Division of labour

- **Codex session (this card):** keep in-scope branches up to date with `main`, watch CI and Codex state, merge (if the operator instructed it) and report.
- **Coordinator:** every content change, every reply on a review thread, every "@codex review" request, every red-CI root cause, every merge conflict. While this card is active the coordinator does not update or merge the in-scope PRs, so the two sessions never race on a head.
- A PR the Codex session cannot advance is **left alone** and listed as blocked in §5. The coordinator receives the same GitHub events and picks it up; the Codex session re-checks it on its next pass.

## 3. Loop (repeat until every in-scope PR is merged or blocked)

Repository: `Joshua-Asante/first-passage`. `main` requires a PR, the `skills (3.12)` status and a branch that is up to date with `main` (strict), so every merge puts every other PR behind.

1. **Read state:** `gh pr view <N> --json headRefOid,mergeStateStatus,mergeable,state`.
2. **Behind `main`:** update it by merge commit, pinned to the head you read:
   `gh api -X PUT repos/Joshua-Asante/first-passage/pulls/<N>/update-branch -f expected_head_sha=<headRefOid>`.
   A 422 means the head moved (usually a coordinator fix); go back to step 1. A merge conflict is a blocker (§4).
3. **CI:** `gh pr checks <N>`. Wait while anything is pending or queued. Clean means every check run on the current head completed `pass` or `skipping`. Anything `fail` or `cancelled` is a blocker (§4); do not re-run it.
4. **Codex state:**
   - no unresolved review thread whose first comment is from `chatgpt-codex-connector` with a P1 or P2 badge (`gh api graphql` on `pullRequest.reviewThreads { isResolved comments(first:1){ nodes { author{login} body } } }`);
   - the latest completed Codex review (the "Codex Review Summary" comment's commit, or a "Didn't find any major issues" comment's reviewed commit) is at or after the PR's last **non-merge** commit. A head that differs from the reviewed commit only by `main` merges passes. If the coordinator pushed a fix and Codex has not reviewed it yet, wait.
5. **Order:** #523 before #527; this card's PR last. Otherwise merge whichever in-scope PR is clean first.
6. **Merge** (only with the operator's direct instruction): `gh pr merge <N> --merge --match-head-commit <headRefOid>`. Never squash or rebase: cited SHAs must stay reachable. Never enable auto-merge.
7. After each merge, `git fetch origin main` and go back to step 1 for every remaining PR. To save wall-clock you may update every remaining ready PR at once (step 2); CI then runs in parallel and the first to go clean merges.

Waiting: `pytest (3.11)` takes about 50 minutes and `qualification-windows` can take longer. Poll no more often than every 5 minutes.

## 4. Blockers (stop on that PR; do not fix)

- a new unresolved Codex P1/P2 thread, or any human reviewer's changes-requested review;
- a failed or cancelled check on the current head;
- a merge conflict on update;
- `mergeable: CONFLICTING` or `mergeStateStatus: BLOCKED` for a reason other than behind/pending checks;
- anything that would need a content edit, a comment, a re-run or a force operation.

Record the blocker (check name and link, or thread link) in §5 and move to the next PR.

## 5. Return

Report to the operator in the Codex session, in this shape, when every in-scope PR is merged or blocked (and on request):

| PR | Final state | Merge SHA | Head merged | Blocker (if any) |
|---|---|---|---|---|

The four-state status is DONE (all merged), DONE_WITH_CONCERNS (some blocked, each named), NEEDS_CONTEXT or BLOCKED.

## 6. Out of bounds

No trade, spend, deploy, arm or vendor contact; no reading or quoting of private Pine or runtime-port sources; no edits to any file; no push to `main`; no PR, branch or thread outside §1.
