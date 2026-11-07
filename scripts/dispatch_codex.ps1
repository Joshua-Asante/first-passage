#Requires -Version 7.0
<#
.SYNOPSIS
Codex CLI dispatch: app-bundled codex.exe, one worktree, a sandbox, a last-message file.
.DESCRIPTION
Uses the Codex app's bundled CLI (...\app\resources\codex.exe); the ~\.codex\.sandbox-bin
copy lacks codex-code-mode-host.exe and cannot run tools. -DryRun runs every check below,
prints the command and the NAMES of the child's environment variables, and launches nothing;
no value is printed. -ReviewBase <ref> runs `codex exec review --base <ref>` instead of a
prompt, forced to the read-only sandbox: the Codex CLI review fallback when a GitHub Codex
review stalls.

What is guarded:
- Credential and environment. Codex starts with a fresh, allowlisted environment (see
  $EnvAllowlist: what Windows, PowerShell, git and the Codex CLI need, plus CODEX_HOME), with
  GH_TOKEN set to FP_AGENT_GH_TOKEN. Nothing else from the caller's environment reaches it:
  not GITHUB_TOKEN, Fly or broker tokens, OPENAI_API_KEY, or any FP_* value. It refuses with no
  agent token (gh would fall back to the operator's stored credential) and refuses a token
  that is not a fine-grained PAT (github_pat_).
- Worktree location. The worktree must be a Git worktree whose top level resolves under
  <repo>\.claude\worktrees\ of the repository it belongs to, and its root must not hold .env.

What is NOT guarded (this is not a sandbox):
- Reads are not confined. Codex runs as the same Windows user as every other agent and the
  operator, and read-only mode does not limit reads to the worktree: it can still open the
  primary checkout, gh's stored credential files and anything else that user can read.
- Prompt and worktree contents are not screened. Codex may read what Claude reads (Joshua,
  2026-11-06). Secret values must never go in a prompt.
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

# The only caller variables the child receives (copied when set). GH_TOKEN is added separately.
$EnvAllowlist = @(
  'SystemRoot', 'SystemDrive', 'windir', 'ComSpec', 'PATH', 'PATHEXT', 'TEMP', 'TMP',
  'USERPROFILE', 'USERNAME', 'HOMEDRIVE', 'HOMEPATH', 'HOME', 'APPDATA', 'LOCALAPPDATA',
  'ProgramData', 'ProgramFiles', 'ProgramFiles(x86)', 'ProgramW6432', 'CommonProgramFiles',
  'OS', 'PROCESSOR_ARCHITECTURE', 'NUMBER_OF_PROCESSORS', 'CODEX_HOME'
)
if (-not $Codex -and (Get-Command Get-AppxPackage -ErrorAction SilentlyContinue)) {
  $pkg = Get-AppxPackage -Name 'OpenAI.Codex*' -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($pkg) { $Codex = Join-Path $pkg.InstallLocation 'app\resources\codex.exe' }
}
$pathCmp = if ($IsWindows) { [StringComparison]::OrdinalIgnoreCase } else { [StringComparison]::Ordinal }
$seps = [char[]]@([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)
function Get-DirKey([string]$p) { [IO.Path]::GetFullPath($p).TrimEnd($seps) + [IO.Path]::DirectorySeparatorChar }

$wt = (Resolve-Path -LiteralPath $Worktree).Path
if (Test-Path -LiteralPath (Join-Path $wt '.env')) { throw "Refusing: $wt contains .env; dispatch from a worktree under .claude\worktrees\." }

# Location: the worktree's top level (as Git resolves it) must sit under <repo>\.claude\worktrees\.
$where = 'dispatch from a Git worktree under <repo>\.claude\worktrees\.'
$top = @(& git -C $wt rev-parse --show-toplevel 2>$null)[0]
$topExit = $LASTEXITCODE
$common = @(& git -C $wt rev-parse --path-format=absolute --git-common-dir 2>$null)[0]
if ($topExit -ne 0 -or $LASTEXITCODE -ne 0 -or -not $top -or -not $common) { throw "Refusing: $wt is not inside a Git checkout; $where" }
$repo = [IO.Path]::GetDirectoryName([IO.Path]::GetFullPath($common.Trim()).TrimEnd($seps))
$root = Get-DirKey ([IO.Path]::Combine($repo, '.claude', 'worktrees'))
$topKey = Get-DirKey $top.Trim()
if (-not $topKey.StartsWith($root, $pathCmp) -or $topKey.Length -le $root.Length) {
  throw "Refusing: $wt is not under $root; $where"
}

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
$childEnv = [ordered]@{}
foreach ($name in $EnvAllowlist) {
  $v = [Environment]::GetEnvironmentVariable($name)
  if ($v) { $childEnv[$name] = $v }
}
if ($DryRun) {
  "codex: $Codex"
  "args: $($codexArgs -join ' | ')"
  "GH_TOKEN: $(if ($token) { 'agent token set' } else { 'not set (FP_AGENT_GH_TOKEN empty; a real run refuses)' })"
  "env: $((@($childEnv.Keys) + @(if ($token) { 'GH_TOKEN' })) -join ', ')"
  return
}
if (-not $token) { throw 'Refusing: FP_AGENT_GH_TOKEN is not set; without it gh falls back to the operator credential.' }
if (-not ($Codex -and (Test-Path -LiteralPath $Codex))) {
  throw 'Codex app CLI not found; pass -Codex <path to ...\app\resources\codex.exe>.'
}
# A new process with a cleared environment; this shell's own environment is not modified.
$psi = [Diagnostics.ProcessStartInfo]::new($Codex)
$psi.UseShellExecute = $false
$psi.WorkingDirectory = $wt
foreach ($a in $codexArgs) { $psi.ArgumentList.Add([string]$a) }
$psi.Environment.Clear()
foreach ($name in $childEnv.Keys) { $psi.Environment[$name] = $childEnv[$name] }
$psi.Environment['GH_TOKEN'] = $token
$proc = [Diagnostics.Process]::Start($psi)
$proc.WaitForExit()
if ($proc.ExitCode -ne 0) { throw "Codex exited $($proc.ExitCode); read $OutputFile before retrying." }
