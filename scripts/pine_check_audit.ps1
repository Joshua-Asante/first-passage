# pine_check_audit.ps1 - PowerShell form of the re-checkable validation hooks
# for scripts/pine_check.py (validated RESOLVED-TRUSTWORTHY 2026-06-23; brief s10).
#
# LOCAL / MANUAL gate (NOT CI): POSTs to the live TradingView Guest endpoint, and
# the oracle regression targets locked .pine that live only in the MAIN working
# tree (gitignored; absent from worktrees/clones) -> skip-if-missing.
# Exit 0 = every runnable hook passed; 1 = a hook failed; 2 = zero oracles ran.
$ErrorActionPreference = 'Continue'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = (Resolve-Path (Join-Path $here '..')).Path
$pc   = Join-Path $root 'scripts/pine_check.py'
$fix  = Join-Path $root 'tests/pine_check_fixtures'
$manifest = Join-Path $root 'core/strategies/MANIFEST.sha256'
$fail = 0
$ran = 0

Write-Output "== fixture assertions =="
python $pc (Join-Path $fix 'good.pine')
if ($LASTEXITCODE -eq 0) { Write-Output "PASS good->0" } else { Write-Output "FAIL good (expected exit 0)"; $fail = 1 }
Start-Sleep -Milliseconds 400
python $pc (Join-Path $fix 'bad.pine')
if ($LASTEXITCODE -eq 1) { Write-Output "PASS bad->1" } else { Write-Output "FAIL bad (expected exit 1)"; $fail = 1 }
Start-Sleep -Milliseconds 400

Write-Output "== ENDPOINT tamper-grep (Guest translate_light facade unchanged) =="
$intact = (Select-String -Path $pc -Pattern 'pine-facade\.tradingview\.com' -Quiet) -and
          (Select-String -Path $pc -Pattern 'translate_light' -Quiet) -and
          (Select-String -Path $pc -Pattern 'user_name=Guest' -Quiet)
if ($intact) { Write-Output "PASS endpoint intact" } else { Write-Output "FAIL endpoint constant changed"; $fail = 1 }

Write-Output "== oracle regression (locked .pine; skip-if-absent - MAIN tree only) =="
$oracle = Get-Content $manifest | ForEach-Object {
  if ($_ -match '^\s*#') { return }
  $parts = $_ -split '\s+', 2
  if ($parts.Count -lt 2) { return }
  $parts[1].Trim()
} | Where-Object { $_ -and $_ -notmatch '_indicator\.pine$' }

foreach ($rel in $oracle) {
  $f = Join-Path $root $rel
  if (-not (Test-Path $f)) { Write-Output "SKIP (absent) $rel"; continue }
  $ran++
  python $pc $f | Out-Null
  if ($LASTEXITCODE -eq 0) { Write-Output "PASS $rel" } else { Write-Output "REGRESSION $rel"; $fail = 1 }
  Start-Sleep -Milliseconds 400
}

$total = @($oracle).Count
if ($ran -eq 0) {
  Write-Output "== audit INCONCLUSIVE: 0/$total oracle .pine present -- this is NOT a PASS =="
  exit 2
}
if ($fail -eq 0) {
  Write-Output "== audit PASS ($ran/$total oracles regression-tested) =="
} else {
  Write-Output "== audit FAIL ($ran/$total oracles regression-tested) =="
}
exit $fail
