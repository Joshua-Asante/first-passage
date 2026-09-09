# Wrapper validation checks: no model calls, network or project mutation.
$ErrorActionPreference = 'Stop'
$pointer = Join-Path $PSScriptRoot 'agent_handoff.md'
$cursor = Join-Path $PSScriptRoot 'dispatch_cursor.ps1'
$claude = Join-Path $PSScriptRoot 'dispatch_claude.ps1'
$fixture = Join-Path ([IO.Path]::GetTempPath()) ('dispatch-wrapper-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $fixture | Out-Null
& $cursor -Workspace $fixture -Pointer $pointer -DryRun
& $claude -Workspace $fixture -Pointer $pointer -AgentCmd (Get-Command python).Source -DryRun
if (Test-Path (Join-Path $fixture '.agent-handoffs')) { throw 'Dry run wrote evidence' }
foreach ($extra in @(@{Plan=$true;ForceCommands=$true}, @{CleanHome=$true}, @{TimeoutSeconds=0}, @{Plan=$true;Ask=$true})) {
  $caught = $false
  try { & $cursor -Workspace $fixture -Pointer $pointer -DryRun @extra } catch { $caught = $true }
  if (!$caught) { throw 'Invalid flags accepted' }
}
$errors = $null
$tokens = $null
foreach ($script in @($cursor, $claude)) {
  $null = [Management.Automation.Language.Parser]::ParseFile($script, [ref]$tokens, [ref]$errors)
  if ($errors.Count) { throw ($errors | Out-String) }
}
Write-Host 'PASS: both dry runs, four rejected flag combinations, both PowerShell syntax checks.'
