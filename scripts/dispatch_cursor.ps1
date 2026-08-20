<#
.SYNOPSIS
  One-call cursor-agent dispatch: create a worktree off a base ref, stage artifacts,
  drop a pointer file, and fire the headless agent. Collapses the 6-step manual dance
  and gives the operator ONE vetted entrypoint to allow-list (safer than allow-listing
  the raw agent binary).

.DESCRIPTION
  Reserve for genuine frozen-spec builds — do NOT dispatch trivial, already-validated
  scripts (run those inline). See memory [[cursor-agent-cli-bridge]].

  One-time setup (operator): review + commit this file, then allow-list ONLY it:
      "PowerShell(& \"$env:LOCALAPPDATA\\...repo...\\scripts\\dispatch_cursor.ps1\" *)"
  or invoke via the Bash tool and allow-list the equivalent Bash(...) prefix.
  The inner `agent.cmd --force` then runs as a subprocess of the vetted script rather
  than as a separately classifier-gated CC action.

  Three modes, same entrypoint:
    default   — one-shot: read the pointer, execute, full write/exec permission.
                Unchanged from before -Plan/-ResumeSessionId existed.
    -Plan     — read-only: read the pointer, propose a plan, make NO edits. Prints
                the session id and writes the full plan JSON to the worktree. Judgment
                (does this plan look right?) stays with whoever reads that output —
                CC or the operator — never auto-approved by this script.
    -ResumeSessionId <id> — continue a prior -Plan session and execute it for real
                (--force). This is the only place write/exec permission is granted
                after a plan review; nothing here auto-chains Plan -> execute.

  Known live bug (2026-08-19, forum.cursor.com/t/.../168129, engineering-acked, no
  fix ETA): on Windows, if MSYSTEM is set (Git Bash always sets it) AND any Claude
  Code PreToolUse hook is registered (e.g. the hookify plugin, enabled per-user in
  ~/.claude/settings.json), Cursor composes its hook-invocation command as PowerShell
  but evaluates it with bash — every shell/terminal tool call inside cursor-agent then
  rejects with a syntax error, silently (exit 0, clean "success" event). File edits are
  a DIFFERENT tool path (afterFileEdit, not beforeShellExecution) and are NOT affected
  — only shell/terminal commands (tests, git, build scripts) are. A -Plan run under the
  bug can silently degrade to guessed-from-docs output instead of a real directory
  read; read $Worktree/CURSOR_PLAN.json's "result" text for hook-rejection language
  before trusting it. Pass -CleanHome to route around it (see that parameter).

.PARAMETER Slug
  Worktree/branch slug. Worktree = <repo>/.worktrees/<Slug>, branch = cursor/<Slug>.

.PARAMETER Pointer
  Path (abs or repo-relative) to the instructions file the agent must read. Copied to
  the worktree root if not already inside it. Required unless -ResumeSessionId is set
  (a resume continues the prior session's own context; nothing new to point at).

.PARAMETER Base
  Base ref for the new worktree branch. Default: origin/main.

.PARAMETER Copy
  Optional artifacts to stage into the worktree, each "src::destRelativeToWorktree".
  e.g. -Copy "C:/tmp/driver.py::lab/analysis/foo/driver.py","C:/tmp/prereg.md::docs/briefs/pre-registration/prereg.md"

.PARAMETER Model
  Optional model override (e.g. "cursor-grok-4.6-high", "sonnet-4-thinking"). Omit to
  use the agent default.

.PARAMETER Plan
  Run in read-only plan mode instead of executing (--mode plan --output-format json,
  no --force). Writes the full response to $Worktree/CURSOR_PLAN.json and prints the
  session id needed for -ResumeSessionId. Mutually exclusive with -ResumeSessionId.

.PARAMETER ResumeSessionId
  Continue a session previously started under -Plan and execute it for real (--force).
  The session id is the "session_id" field in that run's CURSOR_PLAN.json (NOT the
  "chatId" the CLI's own --resume help text implies — verified empirically 2026-08-19,
  the CLI's help wording is wrong). Mutually exclusive with -Plan.

.PARAMETER CleanHome
  Work around the hook-merge bug (see .DESCRIPTION) by pointing cursor-agent at a
  scratch HOME/USERPROFILE that junction-links your real .cursor (keeps auth working)
  but has no .claude directory (so Cursor finds no Claude Code hooks to import — the
  bug's own necessary condition never fires). Scoped to this invocation only: original
  HOME/USERPROFILE are restored in every code path, including on error. The junction
  target persists at $env:TEMP\cursor-clean-home-<Slug> for reuse across calls; if you
  ever delete it by hand, remove the junction first (cmd /c rmdir
  "<dir>\.cursor") — a recursive delete that follows junctions walks into your real
  Cursor config. Does not touch this repo's own .cursor/hooks.json (a different,
  intentional, unaffected hook path — that one uses a plain `python <path>` command,
  never the broken PowerShell-composed wrapper).

.PARAMETER DryRun
  Do everything EXCEPT firing the agent; print the exact command that would run.

.EXAMPLE
  # One-shot (unchanged default behavior)
  ./scripts/dispatch_cursor.ps1 -Slug aegis-6j-wave1-v2 `
     -Pointer .worktrees/aegis-6j-wave1-v2/V2_DISPATCH_INSTRUCTIONS.md -DryRun

.EXAMPLE
  # Plan, review, then execute — two calls
  ./scripts/dispatch_cursor.ps1 -Slug new-packet -Pointer SPEC.md -Plan -CleanHome
  # ... read .worktrees/new-packet/CURSOR_PLAN.json, decide if the plan is right ...
  ./scripts/dispatch_cursor.ps1 -Slug new-packet -ResumeSessionId <session_id from above> -CleanHome
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory)][string]$Slug,
  [string]$Pointer,
  [string]$Base = "origin/main",
  [string[]]$Copy = @(),
  [string]$Model,
  [switch]$Plan,
  [string]$ResumeSessionId,
  [switch]$CleanHome,
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"

if ($Plan -and $ResumeSessionId) {
  throw "-Plan and -ResumeSessionId are mutually exclusive (plan first, then resume in a second call)."
}
if (-not $ResumeSessionId -and -not $Pointer) {
  throw "-Pointer is required unless -ResumeSessionId is given."
}

# Repo root = parent of the scripts/ dir this file lives in.
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$AgentCmd = Join-Path $env:LOCALAPPDATA "cursor-agent\agent.cmd"
if (-not (Test-Path $AgentCmd)) { throw "cursor-agent not found at $AgentCmd" }

$Worktree = Join-Path $RepoRoot ".worktrees/$Slug"
$Branch   = "cursor/$Slug"

# 1. Worktree (reuse if present).
if (Test-Path $Worktree) {
  Write-Host "worktree exists, reusing: $Worktree"
} else {
  Write-Host "creating worktree $Worktree on $Branch off $Base"
  git -C $RepoRoot worktree add $Worktree -b $Branch $Base | Write-Host
}

# 2. Stage artifacts (src::dest). Skipped on a resume — nothing new to stage.
if (-not $ResumeSessionId) {
  foreach ($pair in $Copy) {
    $parts = $pair -split "::", 2
    if ($parts.Count -ne 2) { throw "bad -Copy entry (need src::dest): $pair" }
    $src = $parts[0]; $dst = Join-Path $Worktree $parts[1]
    New-Item -ItemType Directory -Force -Path (Split-Path $dst) | Out-Null
    Copy-Item -LiteralPath $src -Destination $dst -Force
    Write-Host "staged: $($parts[1])"
  }
}

# 3. Pointer file into the worktree root (if external). Skipped on a resume.
if (-not $ResumeSessionId) {
  $pointerResolved = (Resolve-Path $Pointer).Path
  if ($pointerResolved -notlike "$Worktree*") {
    $pointerName = Split-Path $pointerResolved -Leaf
    Copy-Item -LiteralPath $pointerResolved -Destination (Join-Path $Worktree $pointerName) -Force
  } else {
    $pointerName = Split-Path $pointerResolved -Leaf
  }
  Write-Host "pointer: $pointerName"
}

# 4. Build the prompt + args for whichever mode is active.
if ($ResumeSessionId) {
  $prompt = "Proceed with the plan exactly as proposed. No new scope, no re-derivation."
  $agentArgs = @("-p", $prompt, "--workspace", $Worktree, "--resume", $ResumeSessionId,
                 "--force", "--trust", "--output-format", "text")
} elseif ($Plan) {
  $prompt = "Read $pointerName and propose your implementation plan. Analyze only -- " +
            "make no edits and run no mutating commands. If anything in the pointer is " +
            "ambiguous, say so explicitly rather than assuming a default."
  $agentArgs = @("-p", $prompt, "--workspace", $Worktree, "--mode", "plan",
                 "--output-format", "json", "--trust")
} else {
  $prompt = "Read $pointerName and execute exactly"
  $agentArgs = @("-p", $prompt, "--workspace", $Worktree, "--force", "--trust",
                 "--output-format", "text")
}
if ($Model) { $agentArgs += @("--model", $Model) }

if ($DryRun) {
  Write-Host "`n[DRY RUN] would execute:`n  & `"$AgentCmd`" $($agentArgs -join ' ')"
  if ($CleanHome) { Write-Host "[DRY RUN] would also redirect HOME/USERPROFILE per -CleanHome for this call only." }
  Write-Host "worktree staged and ready: $Worktree"
  return
}

# 5. -CleanHome: scope a hook-bug-free HOME/USERPROFILE to just this subprocess call.
$origHome = $env:HOME
$origUserProfile = $env:USERPROFILE
if ($CleanHome) {
  $cleanHomeDir = Join-Path $env:TEMP "cursor-clean-home-$Slug"
  if (-not (Test-Path $cleanHomeDir)) {
    New-Item -ItemType Directory -Force -Path $cleanHomeDir | Out-Null
  }
  $junctionTarget = Join-Path $cleanHomeDir ".cursor"
  if (-not (Test-Path $junctionTarget)) {
    cmd /c mklink /J "$junctionTarget" "$origUserProfile\.cursor" | Write-Host
  }
  Write-Host "clean-home: $cleanHomeDir (.cursor junctioned, no .claude -> hook import finds nothing)"
  $env:HOME = $cleanHomeDir
  $env:USERPROFILE = $cleanHomeDir
}

try {
  if ($Plan) {
    Write-Host "`ndispatching cursor-agent in PLAN mode (read-only, no edits)..."
    $rawOutput = & $AgentCmd @agentArgs
    $planPath = Join-Path $Worktree "CURSOR_PLAN.json"
    $rawOutput | Out-File -FilePath $planPath -Encoding utf8
    try {
      $parsed = $rawOutput | ConvertFrom-Json
      Write-Host "`n== plan captured: $planPath =="
      Write-Host "session_id (pass this to -ResumeSessionId): $($parsed.session_id)"
      if ($parsed.result -match "(?i)hook (blocked|rejected)|syntax error near unexpected token") {
        Write-Host "`n⚠ this plan's output mentions a blocked/rejected tool call -- it may be" -ForegroundColor Yellow
        Write-Host "  degraded (guessed instead of actually executed). Read the full result" -ForegroundColor Yellow
        Write-Host "  text before trusting it. Consider re-running with -CleanHome." -ForegroundColor Yellow
      }
      Write-Host "`n-- result preview --"
      Write-Host $parsed.result
    } catch {
      Write-Host "`n(could not parse JSON output -- raw response written to $planPath, read it directly)"
    }
    Write-Host "`nNEXT: read $planPath in full. If the plan looks right, re-dispatch with:"
    Write-Host "  ./scripts/dispatch_cursor.ps1 -Slug $Slug -ResumeSessionId <session_id above>$(if ($CleanHome) {' -CleanHome'})"
    Write-Host "-- nothing executes until that second call. This script never auto-approves a plan."
  } else {
    Write-Host "`ndispatching cursor-agent (background-safe; results in $Worktree/CURSOR_RETURN.md)..."
    & $AgentCmd @agentArgs
    Write-Host "`n-- dispatch returned. NEXT: read $Worktree/CURSOR_RETURN.md, fable-judge before any commit."
    Write-Host "-- the agent does NOT commit/push/PR; that stays operator/CC-gated."
  }
} finally {
  if ($CleanHome) {
    $env:HOME = $origHome
    $env:USERPROFILE = $origUserProfile
  }
}
