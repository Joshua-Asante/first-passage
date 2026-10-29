---
name: merge-train
description: Use when acting as the merge-train conductor (formerly the merge-train coordinator or PR merge-order agent), the single session that orders and merges open PRs for First Passage. Triggers on "merge train", "merge order", "merge queue", "spin up a merge train conductor", "merge train coordinator", "merge the open PRs when they're ready", or taking over that seat from another session. Gates each merge with scripts/merge_train.py, orders PRs by overlap and stacks, keeps Codex reviews flowing, falls back to the Codex CLI when a GitHub review stalls, and routes conflicts and findings to PR owners. Never commits to PR branches, force-pushes, enables auto-merge or pushes main.
---

# Merge-train conductor

The seat was rebuilt by hand about ten times between 2026-09-26 and 10-25 ([roles research](../../../docs/notes/2026-10-25-repeated-agent-roles.md)), each time from private handoff notes. This skill is the playbook; `scripts/merge_train.py` is the mechanical gate and watcher. Until 2026-10-28 the seat was called the merge-train coordinator. It is complementary to the `coordinator` skill: the coordinator runs the work that produces PRs and hands them over; the conductor orders and merges them (surface-allocation ADR Addendum 2026-10-28, ruling 9).

## Rules: owners, not copies

- **Merge rule and review limit:** [Addendum 2026-10-24b A](../../../docs/adr/2026-07-14-cc-cursor-surface-allocation.md#addendum-2026-10-24b--operator-rulings-conditioned-merge-go-and-credential-custody), with its 2026-10-25 amendment. Summarized in [AGENTS.md §Gate composition authority](../../../AGENTS.md#gate-composition-authority).
- **Who reviews:** Review is cross-agent ([Addendum 2026-10-26](../../../docs/adr/2026-07-14-cc-cursor-surface-allocation.md#addendum-2026-10-26--operator-ruling-cross-agent-review); `docs/operational_rules.md` Rule 5): Codex for Claude-authored PRs, Claude for Codex-authored ones, and Codex for a port of Claude-written code, whoever ports it (same addendum, 2026-10-29). A PR holding both agents' commits needs both reviews clean at the head, and a commit attributed to neither agent goes to Joshua ([Addendum 2026-10-29](../../../docs/adr/2026-07-14-cc-cursor-surface-allocation.md#addendum-2026-10-29--operator-ruling-mixed-author-prs)). No approval, same-agent review or panel counts. `gate` reads only Codex reviews, so a Codex-authored PR merges by hard rule 2's exception, and a mixed-author PR also needs its Claude review confirmed by hand.
- **Talking to cloud sessions:** [task-routing](../task-routing/SKILL.md), "Cloud return channel".

## Hard rules

1. You are the only session that merges in this train. Never commit to a PR branch. The one exception is a conflict-free `gh pr update-branch` on the next PR in line (Joshua's standing permission, 2026-09-30). A conflict or a finding goes to the PR's owner.
2. Merge only on `gate` READY, re-run right before merging. Paste its printed command, which carries the literal 40-hex SHA: `scripts/guard_operator_acts.py` refuses a SHA passed in a variable or `$(...)`. One exception covers a Codex-authored PR, because `gate` reads only Codex reviews. If `gate`'s only reasons are "no Codex review at head" or "Codex review running", a clean Claude review at the exact head satisfies condition (1) (Addendum 2026-10-26). Confirm that review's head SHA by hand, and count that PR's Claude reviews by hand, because `gate` does not: merge only on a clean Claude review within three or on a clean fourth (Rule 6). Then merge with `gh pr merge <n> --repo <owner/repo> --merge --match-head-commit <literal 40-hex head SHA>`. Any other `gate` reason still blocks.
3. Act on `gate`'s HOLD reasons; they apply the review limit. Return the PR to its owner, or ask Joshua where the reason says so.
4. Confirm with Joshua directly, not through a relay, before merging a PR that records his ruling, ratifies, freezes or narrows a decision, or carries a RESULTS verdict. Also hold a PR whose description says he still has to decide something. Exception: a PR whose body declares "consistency-only (surface-allocation ADR Addendum 2026-10-28)" and whose reviewer confirms its diff changes no ruling or rule text needs no direct confirmation.
5. Never `--admin`, auto-merge, force-push, push `main` or `git stash`.

## Procedure

### 1. Snapshot

```bash
gh pr list --state open --json number,title,headRefName,baseRefName    # the queue
python -I scripts/merge_train.py gate 912 913                          # READY / WAIT / HOLD + reasons
python -I scripts/merge_train.py watch --min 911                       # under a Monitor
```

- `--min` is the highest PR number you are *not* coordinating. Older PRs outside this train stay out unless Joshua names them.
- Give the Monitor a timeout longer than `--max-seconds` (default 1680 s, for a 30-minute Monitor).
- `watch` locks its state directory (a second watcher is refused) and reports every PR as NEW on its first poll. It exits by itself before the Monitor would kill it.

### 2. Order

- Fetch first: `git fetch -q origin main pull/<n>/head`.
- **Stacks:** `gate` HOLDs a PR whose base isn't `main`. Retarget it (`gh pr edit <n> --base main`) before its base merges; merged branches are kept, so GitHub never retargets a stack itself.
- **Overlaps:** for PRs that share files (`git diff --name-only origin/main...<head>`), pick an order and test it with `git merge-tree --write-tree --name-only origin/main <head>`. To test against a PR merged ahead of it, build that merge first with `git commit-tree`.
- Put docs PRs before long-suite code PRs.
- When `main` moves, update only the next PR (`gh pr update-branch <n>`). That moves its head, so it needs a fresh review.
  - Never update a PR while its full test suite is running: the push cancels the runs.
  - After a GitHub Actions incident, re-run only runs at the current head. Re-running an old head's run cancels the current one through the workflow's concurrency group.
  - The carry rule (2026-10-03: a review carries when the PR's own blobs are unchanged) predates Addendum 2026-10-24b, and `gate` doesn't apply it.
  - Ask Joshua before relying on the carry rule.

### 3. Keep reviews moving

- Post one `@codex review` on a new PR, and on any new head an owner pushed without requesting one.
- At `STALLED` (a GitHub review "running" at the head for 30 minutes; Joshua, 2026-10-25), run the CLI fallback (step 4). A single re-request has also cleared stalls (#902, #903).

### 4. Codex CLI fallback

```powershell
git -C <repo> worktree add --detach <repo>\.claude\worktrees\codex-review-train <full head sha>   # once; later: git -C <that worktree> checkout --detach <sha>
.\scripts\dispatch_codex.ps1 -Worktree <repo>\.claude\worktrees\codex-review-train -ReviewBase origin/main -OutputFile <scratch>\review_<n>.md
```

- The wrapper runs the app-bundled Codex in a read-only sandbox. It refuses a directory holding `.env`, and it refuses to run without `FP_AGENT_GH_TOKEN` rather than fall back to the operator's token. If it refuses for the token, tell Joshua: the agent PAT is step B1 of his credential checklist.
- Reuse the one worktree. `guard_worktree_evidence.py` can block `git worktree remove`.
- Post the result as a new PR comment whose **first line** is `codex-cli-review:v1 <40-hex head sha> clean` (or `findings`), followed by the review. `gate` counts that line as a Codex review, but only from the repository owner's account and only for that SHA. Never edit a posted result: `gate` HOLDs on an edited one, because the edit hides a review.

`gate` counts reviews from the Codex summary card's edit history. When it HOLDs with "Codex review history incomplete" (an old-format card, an unrecognised Codex reply, a deleted card revision, an edited result, or a receipt the card doesn't account for), count the reviews by hand and ask Joshua before merging.

### 5. Merge

Re-run `gate <n>` and paste its command. After each merge, the other PRs read `mergeStateStatus=UNKNOWN` for a few seconds while GitHub recomputes; re-gate them after that.

### 6. Route

- **Find the owner:** use the PR body's `Cloud-task:` line, or match its branch or title to a session name in `ListAgents`.
- **Conflict:** tell the owner the conflicting file and the `main` commit that caused it. Ask it to merge `origin/main` in (no force-push) and request a fresh review.
- **Finding on a merged PR:** send it to the owner, and also write it to your session group's shared notes folder, so it survives an undelivered message.
- **Owner gone** (archived, or not listed): ask Joshua.
- **Cloud-owned PR:** message the session; it can't reply, so read its PR for the outcome.

### 7. Report each turn

Give a table: PR · head · review · CI · state · next action. Include merge SHAs, and name what is waiting on Joshua.
