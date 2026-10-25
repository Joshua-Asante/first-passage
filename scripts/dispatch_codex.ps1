<#
.SYNOPSIS
Codex CLI dispatch: app-bundled codex.exe, one worktree, a sandbox, a last-message file.
.DESCRIPTION
Uses the Codex app's bundled CLI (...\app\resources\codex.exe); the ~\.codex\.sandbox-bin
copy lacks codex-code-mode-host.exe and cannot run tools. The child gets the agent's own
GitHub token (FP_AGENT_GH_TOKEN -> GH_TOKEN), never the operator's keyring token, and only
for that process. -DryRun prints the command and runs nothing; the token is never printed.
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory)][string]$Worktree,
  [Parameter(Mandatory)][string]$Prompt,
  [Parameter(Mandatory)][string]$OutputFile,
  [ValidateSet('read-only','workspace-write')][string]$Sandbox = 'workspace-write',
  [string]$Model, [string]$Codex, [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
if (-not $Codex) {
  $pkg = Get-AppxPackage -Name 'OpenAI.Codex*' -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($pkg) { $Codex = Join-Path $pkg.InstallLocation 'app\resources\codex.exe' }
}
if (-not $DryRun -and -not ($Codex -and (Test-Path -LiteralPath $Codex))) {
  throw 'Codex app CLI not found; pass -Codex <path to ...\app\resources\codex.exe>.'
}
$wt = (Resolve-Path -LiteralPath $Worktree).Path
if (Test-Path -LiteralPath (Join-Path $wt '.env')) { throw "Refusing: $wt contains .env; dispatch from a worktree under .claude\worktrees\." }
$codexArgs = @('exec', '-C', $wt, '-s', $Sandbox, '-o', $OutputFile)
if ($Model) { $codexArgs += @('-m', $Model) }
$codexArgs += $Prompt
$token = $env:FP_AGENT_GH_TOKEN
if ($DryRun) {
  "codex: $Codex"
  "args: $($codexArgs -join ' | ')"
  "GH_TOKEN: $(if ($token) { 'agent token set' } else { 'not set (FP_AGENT_GH_TOKEN empty)' })"
  return
}
$saved = $env:GH_TOKEN
try {
  if ($token) { $env:GH_TOKEN = $token } else { Remove-Item Env:GH_TOKEN -ErrorAction SilentlyContinue }
  & $Codex @codexArgs
  if ($LASTEXITCODE -ne 0) { throw "Codex exited $LASTEXITCODE; read $OutputFile before retrying." }
} finally {
  if ($null -ne $saved) { $env:GH_TOKEN = $saved } else { Remove-Item Env:GH_TOKEN -ErrorAction SilentlyContinue }
}
