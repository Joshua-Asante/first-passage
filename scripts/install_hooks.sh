#!/usr/bin/env sh
# One-shot: install git pre-commit + pre-push + post-merge hooks (gate runner;
# governance-surface push-collision gate; Pine pin-provenance notice).
#
# Windows: PowerShell `bash` is WSL, not Git Bash; use Git Bash explicitly or
# scripts/install_hooks.bat. Shell templates and this installer are LF-pinned.
#
# pre-merge-commit (the SESSIONS.md duplicate-label gate) was retired in the
# 2026-11 governance cut; a stale installed copy is removed below.
set -eu
ROOT="$(git rev-parse --show-toplevel)"
# Hooks live in the COMMON git dir, shared across all linked worktrees.
# `${ROOT}/.git` is a plain file (gitdir pointer) inside a linked worktree,
# not a directory, so a naive "${ROOT}/.git/hooks/pre-commit" destination
# fails there ("Not a directory"). --git-path resolves correctly from the
# main checkout and from any worktree.
for hook in pre-commit pre-push post-merge; do
  SRC="${ROOT}/scripts/githooks/${hook}"
  DST="$(git rev-parse --git-path "hooks/${hook}")"
  cp "${SRC}" "${DST}"
  chmod +x "${DST}"
  echo "Installed ${DST}"
done
STALE="$(git rev-parse --git-path hooks/pre-merge-commit)"
if [ -f "${STALE}" ]; then
  rm -f "${STALE}"
  echo "Removed retired ${STALE}"
fi
