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
  Launch approval applies to the actual actions and data access, including subprocesses.
  Capture stdout, stderr and exit status for each attempt. Review artifact changes
  and verification evidence before accepting completion.

.PARAMETER ForceCommands
  Explicitly request Cursor --force for an already authorized execution task.
  Omit for normal permission handling. Incompatible with -Plan.

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
  Continue a session previously started under -Plan within existing authority.
  The session id is the "session_id" field in that run's CURSOR_PLAN.json (NOT the
  "chatId" the CLI's own --resume help text implies — verified empirically 2026-08-19,
  the CLI's help wording is wrong). Mutually exclusive with -Plan.

.PARAMETER CleanHome
  Retired. Fails without suppressing hooks; diagnose hook errors with controls intact.

.PARAMETER DryRun
  Describe the intended dispatch without creating worktrees or copying files.

.EXAMPLE
  # Preview a one-shot dispatch
  ./scripts/dispatch_cursor.ps1 -Slug aegis-6j-wave1-v2 `
     -Pointer .worktrees/aegis-6j-wave1-v2/V2_DISPATCH_INSTRUCTIONS.md -DryRun

.EXAMPLE
  # Plan, review, then execute — two calls
  ./scripts/dispatch_cursor.ps1 -Slug new-packet -Pointer SPEC.md -Plan
  # ... read .worktrees/new-packet/CURSOR_PLAN.json, decide if the plan is right ...
  ./scripts/dispatch_cursor.ps1 -Slug new-packet -ResumeSessionId <session_id from above>
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
  [switch]$ForceCommands,
  [string]$AgentCmd = (Join-Path $env:LOCALAPPDATA 'cursor-agent\agent.cmd'),
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"

if ($CleanHome) {
  throw '-CleanHome is retired: suppressing imported hooks is not a routine dispatch repair. Diagnose the exact hook failure with controls intact.'
}
if ($ForceCommands -and $Plan) { throw '-ForceCommands cannot be used with -Plan.' }

if ($Plan -and $ResumeSessionId) {
  throw "-Plan and -ResumeSessionId are mutually exclusive (plan first, then resume in a second call)."
}
if (-not $ResumeSessionId -and -not $Pointer) {
  throw "-Pointer is required unless -ResumeSessionId is given."
}

# Repo root = parent of the scripts/ dir this file lives in.
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
if (-not (Test-Path $AgentCmd)) { throw "cursor-agent not found at $AgentCmd" }

$Worktree = Join-Path $RepoRoot ".worktrees/$Slug"
$Branch   = "cursor/$Slug"

if ($DryRun) {
  Write-Host "Would prepare $Worktree from $Base and launch $AgentCmd (plan=$Plan, resume=$ResumeSessionId, forceCommands=$ForceCommands). No files changed."
  return
}

# 1. Worktree (reuse if present).
if (Test-Path $Worktree) {
  Write-Host "worktree exists, reusing: $Worktree"
} else {
  Write-Host "creating worktree $Worktree on $Branch off $Base"
  git -C $RepoRoot worktree add $Worktree -b $Branch $Base | Write-Host
  if ($LASTEXITCODE -ne 0) { throw "git worktree add failed: exit $LASTEXITCODE" }
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
                 "--trust", "--output-format", "json")
} elseif ($Plan) {
  $prompt = "Read $pointerName and propose your implementation plan. Analyze only -- " +
            "make no edits and run no mutating commands. If anything in the pointer is " +
            "ambiguous, say so explicitly rather than assuming a default."
  $agentArgs = @("-p", $prompt, "--workspace", $Worktree, "--mode", "plan",
                 "--output-format", "json", "--trust")
} else {
  $prompt = "Read $pointerName and execute exactly"
  $agentArgs = @("-p", $prompt, "--workspace", $Worktree, "--trust",
                 "--output-format", "json")
}
if ($ForceCommands) { $agentArgs += '--force' }
if ($Model) { $agentArgs += @("--model", $Model) }

try {
  # Preserve every attempt separately, including nonzero and silent returns.
  $attempt = Join-Path $Worktree ('CURSOR_DISPATCH_' + [guid]::NewGuid().ToString('N'))
  $stdoutPath = "$attempt.stdout.json"
  $stderrPath = "$attempt.stderr.txt"
  & $AgentCmd @agentArgs 1> $stdoutPath 2> $stderrPath
  $agentExit = $LASTEXITCODE
  @{ exit_code=$agentExit; stdout=$stdoutPath; stderr=$stderrPath; workspace=$Worktree; session_id=$ResumeSessionId } |
    ConvertTo-Json | Set-Content "$attempt.result.json" -Encoding utf8
  if ($agentExit -ne 0) { throw "Cursor exited $agentExit. Inspect $attempt.result.json and captured output before retrying." }
  $rawOutput = Get-Content -Raw $stdoutPath
  if ([string]::IsNullOrWhiteSpace($rawOutput)) { throw "Cursor returned no output. Outcome unknown; inspect changes and running processes before retrying. Evidence: $attempt.result.json" }
  $response = $rawOutput | ConvertFrom-Json
  if ($response.is_error -eq $true) { throw "Cursor reported an error: inspect $stdoutPath" }
  if ($response.session_id) {
    Write-Host "session_id: $($response.session_id)"
    @{ exit_code=$agentExit; stdout=$stdoutPath; stderr=$stderrPath; workspace=$Worktree; session_id=$response.session_id } |
      ConvertTo-Json | Set-Content "$attempt.result.json" -Encoding utf8
  }
  if ([string]::IsNullOrWhiteSpace([string]$response.result)) { throw "Cursor response has no result text. Inspect $stdoutPath before retrying." }
  if ($Plan) {
    Write-Host "`ndispatching cursor-agent in PLAN mode (read-only, no edits)..."
    $planPath = Join-Path $Worktree "CURSOR_PLAN.json"
    $rawOutput | Out-File -FilePath $planPath -Encoding utf8
    try {
      $parsed = $rawOutput | ConvertFrom-Json
      Write-Host "`n== plan captured: $planPath =="
      Write-Host "session_id (pass this to -ResumeSessionId): $($parsed.session_id)"
      if ($parsed.result -match "(?i)hook (blocked|rejected)|syntax error near unexpected token") {
        Write-Host "`n⚠ this plan's output mentions a blocked/rejected tool call -- it may be" -ForegroundColor Yellow
        Write-Host "  degraded (guessed instead of actually executed). Read the full result" -ForegroundColor Yellow
        Write-Host "  text before trusting it. Inspect the captured error before retrying." -ForegroundColor Yellow
      }
      Write-Host "`n-- result preview --"
      Write-Host $parsed.result
    } catch {
      Write-Host "`n(could not parse JSON output -- raw response written to $planPath, read it directly)"
    }
    Write-Host "`nNEXT: read $planPath in full. If the plan looks right, re-dispatch with:"
    Write-Host "  ./scripts/dispatch_cursor.ps1 -Slug $Slug -ResumeSessionId <session_id above>"
    Write-Host "-- nothing executes until that second call. This script never auto-approves a plan."
  } else {
    Write-Host "Cursor process returned; completion still requires artifact review."
    Write-Host $response.result
    Write-Host "Process evidence: $attempt.result.json. Verify artifacts and tests before accepting completion."
    if (Test-Path (Join-Path $Worktree 'CURSOR_RETURN.md')) {
      Write-Host "Review CURSOR_RETURN.md against the current attempt; an existing file may be stale."
    } else {
      Write-Host "No CURSOR_RETURN.md found. Review captured result and the packet's expected artifacts."
    }
    Write-Host "-- the agent does NOT commit/push/PR; that stays operator/CC-gated."
  }
} finally {
  # Each attempt retains its evidence for inspection and recovery.
}
