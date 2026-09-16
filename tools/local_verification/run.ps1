#requires -Version 7.3
param(
    [string]$EvidencePath,
    [switch]$Build,
    [ValidateRange(0, 8)][int]$Workers = 0,
    [string[]]$TestPath
)
$ErrorActionPreference = 'Stop'
$PSNativeCommandArgumentPassing = 'Standard'
$PSNativeCommandUseErrorActionPreference = $false
$repo = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$python = (Get-Command python -CommandType Application -ErrorAction Stop | Select-Object -First 1).Source
$runnerArgs = @('-I', (Join-Path $repo 'scripts/docker_verification.py'), '--workers', "$Workers")
if ($EvidencePath) { $runnerArgs += @('--output', $EvidencePath) }
if ($Build) { $runnerArgs += '--build' }
foreach ($test in $TestPath) { $runnerArgs += @('--test-path', $test) }
& $python @runnerArgs
exit $LASTEXITCODE
