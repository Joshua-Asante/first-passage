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

.PARAMETER Slug
  Worktree/branch slug. Worktree = <repo>/.worktrees/<Slug>, branch = cursor/<Slug>.

.PARAMETER Pointer
  Path (abs or repo-relative) to the instructions file the agent must "Read and execute
  exactly". Copied to the worktree root if not already inside it.

.PARAMETER Base
  Base ref for the new worktree branch. Default: origin/main.

.PARAMETER Copy
  Optional artifacts to stage into the worktree, each "src::destRelativeToWorktree".
  e.g. -Copy "C:/tmp/driver.py::lab/analysis/foo/driver.py","C:/tmp/prereg.md::docs/briefs/pre-registration/prereg.md"

.PARAMETER Model
  Optional model override (e.g. "sonnet-4-thinking"). Omit to use the agent default.

.PARAMETER DryRun
  Do everything EXCEPT firing the agent; print the exact command that would run.

.EXAMPLE
  ./scripts/dispatch_cursor.ps1 -Slug aegis-6j-wave1-v2 `
     -Pointer .worktrees/aegis-6j-wave1-v2/V2_DISPATCH_INSTRUCTIONS.md -DryRun
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory)][string]$Slug,
  [Parameter(Mandatory)][string]$Pointer,
  [string]$Base = "origin/main",
  [string[]]$Copy = @(),
  [string]$Model,
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"

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

# 2. Stage artifacts (src::dest).
foreach ($pair in $Copy) {
  $parts = $pair -split "::", 2
  if ($parts.Count -ne 2) { throw "bad -Copy entry (need src::dest): $pair" }
  $src = $parts[0]; $dst = Join-Path $Worktree $parts[1]
  New-Item -ItemType Directory -Force -Path (Split-Path $dst) | Out-Null
  Copy-Item -LiteralPath $src -Destination $dst -Force
  Write-Host "staged: $($parts[1])"
}

# 3. Pointer file into the worktree root (if external).
$pointerResolved = (Resolve-Path $Pointer).Path
if ($pointerResolved -notlike "$Worktree*") {
  $pointerName = Split-Path $pointerResolved -Leaf
  Copy-Item -LiteralPath $pointerResolved -Destination (Join-Path $Worktree $pointerName) -Force
} else {
  $pointerName = Split-Path $pointerResolved -Leaf
}
Write-Host "pointer: $pointerName"

# 4. Build + fire.
$prompt = "Read $pointerName and execute exactly"
$agentArgs = @("-p", $prompt, "--workspace", $Worktree, "--force", "--trust", "--output-format", "text")
if ($Model) { $agentArgs += @("--model", $Model) }

if ($DryRun) {
  Write-Host "`n[DRY RUN] would execute:`n  & `"$AgentCmd`" $($agentArgs -join ' ')"
  Write-Host "worktree staged and ready: $Worktree"
  return
}

Write-Host "`ndispatching cursor-agent (background-safe; results in $Worktree/CURSOR_RETURN.md)..."
& $AgentCmd @agentArgs

Write-Host "`n-- dispatch returned. NEXT: read $Worktree/CURSOR_RETURN.md, fable-judge before any commit."
Write-Host "-- the agent does NOT commit/push/PR; that stays operator/CC-gated."
