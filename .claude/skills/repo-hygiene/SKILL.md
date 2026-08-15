---
name: repo-hygiene
description: Use when pruning merged branches, cleaning git worktrees, clearing orphan .claude/worktrees dirs, recovering from Windows file locks on spent worktrees, or running a git/worktree hygiene pass. Triggers on phrases like "prune branches", "worktree cleanup", "repo hygiene", "delete merged locals", "orphan worktree", or after a batch of PR merges leaves debris. Report-only first — never force-delete without explicit operator confirmation. Does not touch core/, allocations, or Pine.
---

# Repo hygiene — squash-aware prune (report → confirm → delete)

## Why this exists

Hygiene sessions on 2026-07-06, 2026-07-11, and 2026-07-12 repeatedly rediscovered the same debris: squash-merged locals invisible to `git branch --merged`, orphan dirs under `.claude/worktrees/`, Cursor file locks on Windows, and a primary tree left on a spent topic branch after merge. This skill is the playbook; `scripts/repo_hygiene.py` is the mechanical scout.

## Hard rules

1. **Report first. Delete only after explicit operator confirmation** (per branch / per worktree). Finding a branch is merged does **not** override a prior "keep" decision.
2. **Never** `git clean -fdX`, `git push --force`, or `git branch -D` unless the operator explicitly orders the destructive form.
3. Prefer `git branch -d` (safe) over `-D`. Prefer `git worktree remove` over manual folder deletes; on Windows "Filename too long" / file-lock failures, stop and ask — do not invent a force path without confirmation.
4. Do not delete a branch that is checked out in any worktree.
5. Do not edit files in the **primary** tree when the session's intended checkout is a linked worktree — verify `git rev-parse --show-toplevel` matches the worktree you mean.

## Procedure

### 1. Scout

```bash
python scripts/repo_hygiene.py
# optional network refresh:
python scripts/repo_hygiene.py --fetch
# machine-readable:
python scripts/repo_hygiene.py --json
```

Read: primary vs `origin/main` lag, linked worktrees, orphan dirs, merged-local candidates (gh squash-aware when `gh` is available).

### 2. Classify

| Finding | Default disposition |
|---|---|
| Local branch, PR merged, not checked out | Candidate for `git branch -d` after confirm |
| Local branch, "keep" previously requested | Leave; re-confirm with new evidence before deleting |
| Linked worktree, branch merged + clean | Candidate for `git worktree remove` then `git branch -d` |
| Orphan dir under `.claude/worktrees/` | Close Cursor handles → remove dir; `git worktree prune` |
| Primary on spent topic, behind `origin/main` | Checkout/ff `main` first; then prune |

### 3. Confirm + delete (one at a time)

Show the candidate list. Ask which to remove. For each approved item:

```bash
git worktree remove <path>          # if linked worktree
git branch -d <name>                # local
git push origin --delete <name>     # only if operator also wants remote gone
git worktree prune --verbose
```

### 4. Verify

```bash
git worktree list
git status -sb
python scripts/repo_hygiene.py
```

## Related

- `docs/notes/cleanup/2026-07-11-worktree-temp-cleanup.md` — worked example
- `docs/SESSIONS.md` 2026-07-12 hygiene entry — squash-merge + primary-tree path mistake
- Slash command `/post-merge` — post-merge doc/board checklist (orthogonal to prune)
