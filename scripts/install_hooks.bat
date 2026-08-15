@echo off
setlocal enabledelayedexpansion
for /f "usebackq delims=" %%i in (`git rev-parse --show-toplevel`) do set "ROOT=%%i"
rem Hooks live in the COMMON git dir, shared across all linked worktrees.
rem "%ROOT%\.git" is a plain file (gitdir pointer) inside a linked worktree,
rem not a directory, so a naive "%ROOT%\.git\hooks\pre-commit" destination
rem fails there. --git-path resolves correctly from the main checkout and
rem from any worktree.
rem pre-merge-commit is NOT redundant with pre-commit: git does not run
rem pre-commit when it auto-creates a merge commit (measured 2026-08-09), and
rem docs/SESSIONS.md is merge=union, so the merge that produces a duplicate
rem session label is clean by construction. Omitting it here silently disables
rem that gate on Windows -- which CLAUDE.md points at as the PREFERRED path.
for %%H in (pre-commit pre-merge-commit pre-push post-merge) do (
  for /f "usebackq delims=" %%h in (`git rev-parse --git-path hooks/%%H`) do set "DST=%%h"
  copy /Y "%ROOT%\scripts\githooks\%%H" "!DST!" >nul
  echo Installed !DST!
)
echo Git for Windows runs these hooks via sh; keep the POSIX shebangs in the templates.
