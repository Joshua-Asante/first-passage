---
name: babysit
description: "Monitor and maintain a pull request after the agent opens or updates it. Use automatically whenever the agent creates a PR, or when asked to watch, babysit, shepherd, or follow a PR: keep polling checks and review activity, diagnose and fix CI failures, rebase conflicts, address actionable review comments, push repairs, and continue until the PR is merge-ready with required checks green and no feedback left to address."
---

# Babysit a pull request

Own the PR from creation through merge readiness. Do not merely report failures or promise to check later: inspect, repair, push, and verify.

## Start monitoring

1. Identify the PR created from the current branch. Record its number, URL, base branch, and head branch.
2. Read repository instructions before changing files. Keep unrelated local changes intact.
3. Inspect the complete current state:
   - required and pending checks, including failure logs;
   - mergeability and base-branch drift;
   - reviews, inline comments, conversation threads, and general comments;
   - new commits or changes made by other actors.
4. Maintain a short ledger of each check failure and review thread as pending, addressed, obsolete, or non-actionable, with evidence.

Prefer the repository's configured hosting CLI and API. For GitHub, begin with `gh pr view`, `gh pr checks`, and `gh api`; do not rely on a single summary command when inline review threads or check logs require separate queries.

## Monitoring loop

Repeat this loop until the exit criteria pass:

1. **Refresh before acting.** Fetch the remote and reload checks, mergeability, reviews, comments, and threads. Never act on a stale snapshot.
2. **Resolve conflicts.** If the PR conflicts with its base, rebase the head branch onto the latest base unless repository instructions require another strategy. Resolve conflicts by preserving both intended behaviors, run relevant tests, and push with `--force-with-lease`, never an unguarded force push.
3. **Repair CI.** For every failing required check, open the failing job and step logs, reproduce the failure locally when possible, fix the root cause, run the narrow relevant check and any required broader suite, commit, and push. Do not rerun a deterministic failure without a reason. Rerun infrastructure-only flakes when the platform permits and record why no code change was needed.
4. **Address feedback.** Read all new review and discussion activity. Implement every actionable request, test it, commit, and push. Reply with the concrete change and commit or explain, with evidence, why a comment is already satisfied or not actionable. Do not dismiss, hide, or resolve another person's thread merely to make the queue appear empty.
5. **Wait for the new revision.** Monitor pending checks to completion. Poll at a moderate interval when no watch command is available; avoid API-hammering busy loops.
6. **Restart on change.** Any new commit, base update, failed check, review, or comment invalidates the previous snapshot. Return to step 1.

When blocked by missing credentials, unavailable infrastructure, or a decision only a human can make, report the exact blocker and requested action, but remain in the monitoring workflow and resume polling after the blocker can clear. Do not describe a blocked PR as complete.

## Exit criteria

Stop only after a fresh, post-push snapshot confirms all of the following:

- the PR is open and mergeable with no conflicts;
- every required check has completed successfully (allowed neutral/skipped conclusions count only when branch protection accepts them);
- no check is pending, queued, failing, timed out, or cancelled in a way that blocks merging;
- all submitted reviews and all visible discussion or inline threads have been read;
- every actionable comment is implemented or answered with evidence, and no change request remains unsatisfied;
- the local ledger has no pending item.

Run one final full refresh after reaching this state so a late event cannot race the completion report. Then report the PR URL, head commit, check result, mergeability, and disposition of review feedback. Do not claim the PR is merged unless it actually is.
