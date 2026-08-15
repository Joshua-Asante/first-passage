# Q-CAPALLOC-2 §8 protocol — legacy sentinel, then 6-cell drift grid.
# Harness: run_capalloc.py verbatim (CLI flags only). Outputs land here, not on measured.json permanently.
$ErrorActionPreference = "Stop"
# $PSScriptRoot = .../lab/analysis/c1_capalloc_2026-07-27/capalloc2
$Out = $PSScriptRoot
$Here = Resolve-Path (Join-Path $PSScriptRoot "..")
$Root = Resolve-Path (Join-Path $PSScriptRoot "..\..\..\..")
$Py = "python"
$Runner = Join-Path $Here "run_capalloc.py"
$Measured = Join-Path $Here "measured.json"
$Backup = Join-Path $Out "measured_capalloc1_backup.json"
$GridLog = Join-Path $Out "grid.log"

Set-Location $Root
$stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"repo=$Root runner=$Runner" | Out-File $GridLog -Encoding utf8
"=== Q-CAPALLOC-2 grid start $stamp ===" | Tee-Object -FilePath $GridLog -Append

function Invoke-Cell {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string[]]$CliArgs
    )
    $log = Join-Path $Out "$Name.log"
    $t0 = Get-Date
    "--- $Name start $($t0.ToString('u')) args: $($CliArgs -join ' ') ---" | Tee-Object -FilePath $GridLog -Append
    & $Py $Runner @CliArgs 2>&1 | Tee-Object -FilePath $log
    if ($LASTEXITCODE -ne 0) { throw "FAIL $Name exit=$LASTEXITCODE" }
    Copy-Item $Measured (Join-Path $Out "$Name.json") -Force
    $dt = (Get-Date) - $t0
    "--- $Name done in $([int]$dt.TotalMinutes)m $($dt.Seconds)s ---" | Tee-Object -FilePath $GridLog -Append
}

# §8.2 Legacy drift arm first (fail-closed sentinel)
Invoke-Cell -Name "legacy_sentinel" -CliArgs @("--funded-ladder", "legacy", "--payout-min", "1000")

# §8.3 Six drift cells at verified ladder (default --funded-ladder verified)
$cells = @(
    @{ Name = "w150_p0";   CliArgs = @("--win-min", "150", "--payout-min", "0") },
    @{ Name = "w200_p0";   CliArgs = @("--win-min", "200", "--payout-min", "0") },
    @{ Name = "w250_p0";   CliArgs = @("--win-min", "250", "--payout-min", "0") },
    @{ Name = "w150_p250"; CliArgs = @("--win-min", "150", "--payout-min", "250") },
    @{ Name = "w200_p250"; CliArgs = @("--win-min", "200", "--payout-min", "250") },
    @{ Name = "w250_p250"; CliArgs = @("--win-min", "250", "--payout-min", "250") }
)
foreach ($c in $cells) {
    Invoke-Cell -Name $c.Name -CliArgs $c.CliArgs
}

# Restore CAPALLOC-1 measured.json so we never leave the parent's record overwritten
if (Test-Path $Backup) {
    Copy-Item $Backup $Measured -Force
    "restored measured.json from CAPALLOC-1 backup" | Tee-Object -FilePath $GridLog -Append
}

"=== Q-CAPALLOC-2 grid COMPLETE $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ===" | Tee-Object -FilePath $GridLog -Append
