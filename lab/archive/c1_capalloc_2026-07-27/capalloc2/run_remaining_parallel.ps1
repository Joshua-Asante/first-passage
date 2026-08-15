# After w250_p0 (slow path) finishes: run the 3 PAYOUT_MIN=250 cells in parallel
# via run_cell_fast.py (SENSITIVITY=[]). Does not touch run_capalloc.py.
$ErrorActionPreference = "Stop"
$Out = $PSScriptRoot
$Root = Resolve-Path (Join-Path $PSScriptRoot "..\..\..\..")
$Fast = Join-Path $Out "run_cell_fast.py"
$Backup = Join-Path $Out "measured_capalloc1_backup.json"
$Measured = Resolve-Path (Join-Path $PSScriptRoot "..\measured.json")
$GridLog = Join-Path $Out "grid_fast.log"

Set-Location $Root
$stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"=== CAPALLOC-2 fast parallel remaining $stamp ===" | Out-File $GridLog -Encoding utf8

$jobs = @(
    @{ Name = "w150_p250"; Cli = @("--win-min", "150", "--payout-min", "250") },
    @{ Name = "w200_p250"; Cli = @("--win-min", "200", "--payout-min", "250") },
    @{ Name = "w250_p250"; Cli = @("--win-min", "250", "--payout-min", "250") }
)

$procs = @()
foreach ($j in $jobs) {
    $log = Join-Path $Out "$($j.Name).log"
    $json = Join-Path $Out "$($j.Name).json"
    $argList = @($Fast, "--out", $json) + $j.Cli
    "--- spawn $($j.Name) $($j.Cli -join ' ') ---" | Tee-Object -FilePath $GridLog -Append
    $p = Start-Process -FilePath "python" -ArgumentList $argList `
        -RedirectStandardOutput $log -RedirectStandardError (Join-Path $Out "$($j.Name).err.log") `
        -PassThru -NoNewWindow
    $procs += @{ Name = $j.Name; Proc = $p; Json = $json }
}

$failed = @()
foreach ($p in $procs) {
    Wait-Process -Id $p.Proc.Id
    $code = $p.Proc.ExitCode
    if ($code -ne 0 -or -not (Test-Path $p.Json)) {
        $failed += "$($p.Name) exit=$code"
        "--- FAIL $($p.Name) exit=$code ---" | Tee-Object -FilePath $GridLog -Append
    } else {
        "--- OK $($p.Name) ---" | Tee-Object -FilePath $GridLog -Append
    }
}

if (Test-Path $Backup) {
    Copy-Item $Backup $Measured -Force
    "restored measured.json from CAPALLOC-1 backup" | Tee-Object -FilePath $GridLog -Append
}

if ($failed.Count -gt 0) {
    "FAILED: $($failed -join '; ')" | Tee-Object -FilePath $GridLog -Append
    exit 1
}
"=== CAPALLOC-2 fast parallel COMPLETE $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ===" | Tee-Object -FilePath $GridLog -Append
