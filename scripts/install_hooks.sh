#!/usr/bin/env sh
# One-shot: install git pre-commit + pre-merge-commit + pre-push + post-merge
# hooks (vendor SHA256SUMS validation; governance-surface push-collision gate;
# SESSIONS.md union-merge debris normalization + duplicate-label gate).
#
# Windows: PowerShell `bash` is WSL, not Git Bash — this file is CRLF; prefer
# scripts/install_hooks.bat (same warning as CLAUDE.md §Vendor-data integrity).
#
# pre-merge-commit is separate from pre-commit on purpose: pre-commit does not
# run when git auto-creates a merge commit (measured 2026-08-09), which is
# exactly the union merge that produces a duplicate session label.
set -eu
ROOT="$(git rev-parse --show-toplevel)"
# Hooks live in the COMMON git dir, shared across all linked worktrees.
# `${ROOT}/.git` is a plain file (gitdir pointer) inside a linked worktree,
# not a directory, so a naive "${ROOT}/.git/hooks/pre-commit" destination
# fails there ("Not a directory"). --git-path resolves correctly from the
# main checkout and from any worktree.
for hook in pre-commit pre-merge-commit pre-push post-merge; do
  SRC="${ROOT}/scripts/githooks/${hook}"
  DST="$(git rev-parse --git-path "hooks/${hook}")"
  cp "${SRC}" "${DST}"
  chmod +x "${DST}"
  echo "Installed ${DST}"
done
