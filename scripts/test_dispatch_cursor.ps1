# Isolated launcher tests: no external agent, network, or repository mutation.
$ErrorActionPreference = 'Stop'
$fixture = Join-Path ([IO.Path]::GetTempPath()) ('dispatch-test-' + [guid]::NewGuid().ToString('N'))
$scripts = New-Item -ItemType Directory -Path (Join-Path $fixture 'scripts')
Copy-Item (Join-Path $PSScriptRoot 'dispatch_cursor.ps1') $scripts.FullName
$launcher = Join-Path $scripts.FullName 'dispatch_cursor.ps1'
$worker = Join-Path $fixture 'worker.ps1'
@'
if ($env:DISPATCH_TEST_CASE -eq 'nonzero') { $global:LASTEXITCODE=7; return }
if ($env:DISPATCH_TEST_CASE -eq 'empty') { $global:LASTEXITCODE=0; return }
if ($env:DISPATCH_TEST_CASE -eq 'malformed') { 'not json'; $global:LASTEXITCODE=0; return }
if ($env:DISPATCH_TEST_CASE -eq 'error') { '{"is_error":true,"result":"denied"}'; $global:LASTEXITCODE=0; return }
if ($env:DISPATCH_TEST_CASE -eq 'missing') { '{"session_id":"test-session"}'; $global:LASTEXITCODE=0; return }
if ($args -contains '--force') { throw 'Unexpected force flag' }
'{"session_id":"test-session","result":"fixture complete","is_error":false}'
$global:LASTEXITCODE=0
'@ | Set-Content $worker -Encoding utf8
& $launcher -Slug preview -Pointer unused -AgentCmd $worker -DryRun
if (Test-Path (Join-Path $fixture '.worktrees')) { throw 'Dry run mutated filesystem' }
foreach ($case in @('nonzero','empty','malformed','error','missing','success')) {
    $env:DISPATCH_TEST_CASE = $case
    $tree = New-Item -ItemType Directory -Path (Join-Path $fixture ".worktrees/$case")
    $caught = $false
    try { & $launcher -Slug $case -ResumeSessionId test-session -AgentCmd $worker } catch { $caught=$true }
    if ($caught -ne ($case -ne 'success')) { throw "Unexpected disposition for $case" }
    $record = Get-ChildItem $tree.FullName -Filter '*.result.json'
    if (@($record).Count -ne 1) { throw "Missing process evidence for $case" }
    $data = Get-Content -Raw $record.FullName | ConvertFrom-Json
    if ($case -eq 'nonzero' -and $data.exit_code -ne 7) { throw 'Lost exit code' }
    if (!(Test-Path $data.stdout) -or !(Test-Path $data.stderr)) { throw 'Missing streams' }
    Write-Host "PASS $case"
}
Remove-Item Env:DISPATCH_TEST_CASE
Write-Host "PASS dry-run; fixtures retained at $fixture"
