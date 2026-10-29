<#
.SYNOPSIS
Codex CLI dispatch: app-bundled codex.exe, one worktree, a sandbox, a last-message file.
.DESCRIPTION
Uses the Codex app's bundled CLI (...\app\resources\codex.exe); the ~\.codex\.sandbox-bin
copy lacks codex-code-mode-host.exe and cannot run tools. The child authenticates to GitHub
only with the agent's own token (FP_AGENT_GH_TOKEN -> GH_TOKEN; GITHUB_TOKEN cleared). With
no agent token it refuses to launch, because gh would fall back to the operator's stored
credential, and it refuses a token that is not a fine-grained PAT. -DryRun prints the command and runs nothing; the token is never printed.
-ReviewBase <ref> runs `codex exec review --base <ref>` instead of a prompt, forced to the
read-only sandbox: the Codex CLI review fallback the merge-train skill uses when a GitHub
Codex review stalls.
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory)][string]$Worktree,
  [string]$Prompt,
  [Parameter(Mandatory)][string]$OutputFile,
  [ValidateSet('read-only','workspace-write')][string]$Sandbox = 'workspace-write',
  [string]$Model, [string]$Codex, [string]$ReviewBase, [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
if (-not $Codex -and (Get-Command Get-AppxPackage -ErrorAction SilentlyContinue)) {
  $pkg = Get-AppxPackage -Name 'OpenAI.Codex*' -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($pkg) { $Codex = Join-Path $pkg.InstallLocation 'app\resources\codex.exe' }
}
$wt = (Resolve-Path -LiteralPath $Worktree).Path
if (Test-Path -LiteralPath (Join-Path $wt '.env')) { throw "Refusing: $wt contains .env; dispatch from a worktree under .claude\worktrees\." }
if ($ReviewBase) {
  # `review --base` takes no prompt argument.
  $codexArgs = @('exec', '-C', $wt, '-s', 'read-only', 'review', '--base', $ReviewBase, '-o', $OutputFile)
  if ($Model) { $codexArgs += @('-m', $Model) }
} else {
  if (-not $Prompt) { throw 'Pass -Prompt, or -ReviewBase <ref> for a review.' }
  $codexArgs = @('exec', '-C', $wt, '-s', $Sandbox, '-o', $OutputFile)
  if ($Model) { $codexArgs += @('-m', $Model) }
  $codexArgs += $Prompt
}
$token = $env:FP_AGENT_GH_TOKEN
# The agent identity is a fine-grained PAT; an OAuth or classic token here is likely the operator's.
if ($token -and -not $token.StartsWith('github_pat_')) {
  throw 'Refusing: FP_AGENT_GH_TOKEN is not a fine-grained PAT (github_pat_), so it may be the operator credential.'
}
if ($DryRun) {
  "codex: $Codex"
  "args: $($codexArgs -join ' | ')"
  "GH_TOKEN: $(if ($token) { 'agent token set' } else { 'not set (FP_AGENT_GH_TOKEN empty; a real run refuses)' })"
  return
}
if (-not $token) { throw 'Refusing: FP_AGENT_GH_TOKEN is not set; without it gh falls back to the operator credential.' }
if (-not ($Codex -and (Test-Path -LiteralPath $Codex))) {
  throw 'Codex app CLI not found; pass -Codex <path to ...\app\resources\codex.exe>.'
}
$saved = @{ GH_TOKEN = $env:GH_TOKEN; GITHUB_TOKEN = $env:GITHUB_TOKEN }
try {
  $env:GH_TOKEN = $token
  Remove-Item Env:GITHUB_TOKEN -ErrorAction SilentlyContinue
  & $Codex @codexArgs
  if ($LASTEXITCODE -ne 0) { throw "Codex exited $LASTEXITCODE; read $OutputFile before retrying." }
} finally {
  foreach ($name in $saved.Keys) {
    if ($null -ne $saved[$name]) { Set-Item "Env:$name" $saved[$name] } else { Remove-Item "Env:$name" -ErrorAction SilentlyContinue }
  }
}
