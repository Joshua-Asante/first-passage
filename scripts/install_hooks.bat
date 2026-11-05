@echo off
setlocal enabledelayedexpansion
for /f "usebackq delims=" %%i in (`git rev-parse --show-toplevel`) do set "ROOT=%%i"
rem Hooks live in the COMMON git dir, shared across all linked worktrees.
rem "%ROOT%\.git" is a plain file (gitdir pointer) inside a linked worktree,
rem not a directory, so a naive "%ROOT%\.git\hooks\pre-commit" destination
rem fails there. --git-path resolves correctly from the main checkout and
rem from any worktree.
rem pre-merge-commit (the SESSIONS.md duplicate-label gate) was retired in the
rem 2026-11 governance cut; a stale installed copy is removed below.
for %%H in (pre-commit pre-push post-merge) do (
  for /f "usebackq delims=" %%h in (`git rev-parse --git-path hooks/%%H`) do set "DST=%%h"
  copy /Y "%ROOT%\scripts\githooks\%%H" "!DST!" >nul
  echo Installed !DST!
)
for /f "usebackq delims=" %%h in (`git rev-parse --git-path hooks/pre-merge-commit`) do set "STALE=%%h"
if exist "!STALE!" (
  del /F "!STALE!"
  echo Removed retired !STALE!
)
echo Git for Windows runs these hooks via sh; keep the POSIX shebangs in the templates.
