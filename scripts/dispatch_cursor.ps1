<#
.SYNOPSIS
Prepare a Cursor worktree and use the durable agent_handoff runner.
.DESCRIPTION
See agent_handoff.md. Use -Workspace for an existing directory or -Slug for
.worktrees/<Slug> on cursor/<Slug>. Resume needs a receipt and unchanged packet.
ForceCommands explicitly selects --force. CleanHome is retired.
#>
[CmdletBinding()]
param(
  [string]$Slug, [string]$Workspace, [Parameter(Mandatory)][string]$Pointer,
  [string]$Base = 'origin/main', [string[]]$Copy = @(),
  [string[]]$InputFile = @(), [string[]]$ExpectedOutput = @(),
  [string[]]$RequiredCheck = @(), [string[]]$AddDirectory = @(),
  [string]$Model, [switch]$Plan, [switch]$Ask,
  [string]$ResumeSessionId, [string]$ResumeRequestId, [string]$MessageFile,
  [string]$RequestId, [double]$TimeoutSeconds = 900,
  [switch]$CleanHome, [switch]$ForceCommands, [string]$AgentCmd, [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
if ($CleanHome) { throw '-CleanHome is retired; diagnose hooks with controls intact.' }
if ($Plan -and $Ask) { throw 'Choose -Plan or -Ask.' }
if ($ForceCommands -and ($Plan -or $Ask)) { throw '-ForceCommands is only for execution.' }
if ($ResumeSessionId -and $ResumeRequestId) { throw 'Choose one resume identifier.' }
if ($TimeoutSeconds -le 0 -or [double]::IsNaN($TimeoutSeconds) -or [double]::IsInfinity($TimeoutSeconds)) { throw 'Timeout must be finite and positive.' }
if ($Workspace -and $Slug) { throw 'Choose -Workspace or -Slug.' }
if (!$Workspace -and $Slug -notmatch '^[a-zA-Z0-9][a-zA-Z0-9_-]*$') { throw 'Supply -Workspace or a simple -Slug.' }
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$existingWorkspace = [bool]$Workspace
if (!$Workspace) { $Workspace = Join-Path $RepoRoot ".worktrees/$Slug" }
$pointerPath = (Resolve-Path -LiteralPath $Pointer).Path
if ($DryRun) {
  Write-Host "Would dispatch $pointerPath to Cursor in $Workspace. No files changed."
  return
}
if ($existingWorkspace) {
  $Workspace = (Resolve-Path -LiteralPath $Workspace).Path
} elseif (!(Test-Path -LiteralPath $Workspace)) {
  if ($ResumeRequestId -or $ResumeSessionId) { throw 'Resume workspace is missing.' }
  git -C $RepoRoot worktree add $Workspace -b "cursor/$Slug" $Base
  if ($LASTEXITCODE -ne 0) { throw "Worktree creation failed: $LASTEXITCODE" }
} else {
  $actual = git -C $Workspace rev-parse --show-toplevel
  if ($LASTEXITCODE -ne 0 -or [IO.Path]::GetFullPath($actual) -ne [IO.Path]::GetFullPath($Workspace)) { throw 'Existing directory is not the expected worktree.' }
  $branch = git -C $Workspace branch --show-current
  if ($LASTEXITCODE -ne 0 -or $branch -ne "cursor/$Slug") { throw 'Existing worktree branch mismatch.' }
}
if (($ResumeRequestId -or $ResumeSessionId) -and $Copy.Count) { throw 'Do not stage new copies during resume.' }
$mode = if ($Plan) {'plan'} elseif ($Ask) {'ask'} else {'execute'}
$runnerArgs = @((Join-Path $PSScriptRoot 'agent_handoff.py'), 'run', '--provider', 'cursor', '--workspace', $Workspace,
                '--pointer', $pointerPath, '--mode', $mode, '--timeout-seconds', $TimeoutSeconds.ToString([Globalization.CultureInfo]::InvariantCulture))
foreach ($item in $InputFile) { $runnerArgs += @('--input', (Resolve-Path -LiteralPath $item).Path) }
foreach ($item in $Copy) { $runnerArgs += @('--copy', $item) }
foreach ($item in $ExpectedOutput) { $runnerArgs += @('--expected-output', $item) }
foreach ($item in $RequiredCheck) { $runnerArgs += @('--required-check', $item) }
foreach ($item in $AddDirectory) { $runnerArgs += @('--add-dir', $item) }
if ($Model) { $runnerArgs += @('--model', $Model) }
if ($ResumeSessionId) { $runnerArgs += @('--resume-session', $ResumeSessionId) }
if ($ResumeRequestId) { $runnerArgs += @('--resume-request', $ResumeRequestId) }
if ($MessageFile) { $runnerArgs += @('--message-file', $MessageFile) }
if ($RequestId) { $runnerArgs += @('--request-id', $RequestId) }
if ($ForceCommands) { $runnerArgs += '--force-commands' }
if ($AgentCmd) { $runnerArgs += @('--command-json', (ConvertTo-Json -InputObject @($AgentCmd) -Compress)) }
& python @runnerArgs
if ($LASTEXITCODE -ne 0) { throw "Dispatch incomplete (exit $LASTEXITCODE); inspect receipt before retrying." }
