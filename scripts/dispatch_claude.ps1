<#
.SYNOPSIS
Claude CLI handoffs with persistence, request receipts and return validation.
.DESCRIPTION
See agent_handoff.md. Existing settings/hooks stay active. No permission bypass.
Ask uses Read/Glob/Grep. Plan uses plan permissions. Execution uses existing
permissions and an optional explicit AllowedTools list.
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory)][string]$Workspace,
  [Parameter(Mandatory)][string]$Pointer,
  [ValidateSet('execute','plan','ask')][string]$Mode = 'execute',
  [string]$ResumeRequestId, [string]$RequestId, [string]$MessageFile,
  [string[]]$InputFile = @(), [string[]]$ExpectedOutput = @(),
  [string[]]$RequiredCheck = @(), [string[]]$AddDirectory = @(),
  [string]$AllowedTools, [string]$Model, [double]$TimeoutSeconds = 900,
  [string]$AgentCmd, [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
$runnerArgs = @((Join-Path $PSScriptRoot 'agent_handoff.py'), 'run', '--provider', 'claude', '--workspace', $Workspace,
                '--pointer', (Resolve-Path -LiteralPath $Pointer).Path, '--mode', $Mode,
                '--timeout-seconds', $TimeoutSeconds.ToString([Globalization.CultureInfo]::InvariantCulture))
foreach ($item in $InputFile) { $runnerArgs += @('--input', (Resolve-Path -LiteralPath $item).Path) }
foreach ($item in $ExpectedOutput) { $runnerArgs += @('--expected-output', $item) }
foreach ($item in $RequiredCheck) { $runnerArgs += @('--required-check', $item) }
foreach ($item in $AddDirectory) { $runnerArgs += @('--add-dir', $item) }
if ($ResumeRequestId) { $runnerArgs += @('--resume-request', $ResumeRequestId) }
if ($RequestId) { $runnerArgs += @('--request-id', $RequestId) }
if ($MessageFile) { $runnerArgs += @('--message-file', $MessageFile) }
if ($AllowedTools) { $runnerArgs += @('--allowed-tools', $AllowedTools) }
if ($Model) { $runnerArgs += @('--model', $Model) }
if ($AgentCmd) { $runnerArgs += @('--command-json', (ConvertTo-Json -InputObject @($AgentCmd) -Compress)) }
if ($DryRun) { $runnerArgs += '--dry-run' }
& python @runnerArgs
if ($LASTEXITCODE -ne 0) { throw "Dispatch incomplete (exit $LASTEXITCODE); inspect receipt before retrying." }
