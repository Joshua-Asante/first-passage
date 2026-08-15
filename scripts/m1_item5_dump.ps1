# M1 item-5 host dump (Windows / PowerShell)
#
# fly ssh console -C often exits 1 with "Error: The handle is invalid." AFTER
# printing good output — judge by content, not exit code. This helper strips
# that trailer and writes clean JSONL / log text for m1_item5_capture.py.
#
# Usage (from repo root):
#   powershell -File scripts/m1_item5_dump.ps1
#   powershell -File scripts/m1_item5_dump.ps1 -OutDir $env:TEMP\m1_item5
#
# Then:
#   python scripts/m1_item5_capture.py <OutDir>\c1_rail_events.jsonl --preflight `
#       --audit-log <OutDir>\c1_rail_audit.log
#   python scripts/m1_item5_capture.py <OutDir>\c1_rail_events.jsonl --latest

param(
    [string]$App = "c1-rail",
    [string]$OutDir = $(Join-Path $env:TEMP "m1_item5")
)

$ErrorActionPreference = "Continue"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

function Invoke-FlyDump([string]$RemoteCmd, [string]$DestPath, [scriptblock]$Filter) {
    Write-Host ">> fly ssh console -a $App -C `"$RemoteCmd`""
    $raw = & fly ssh console -a $App -C $RemoteCmd 2>&1 | ForEach-Object { "$_" }
    $kept = @($raw | Where-Object $Filter)
    Set-Content -Path $DestPath -Value $kept -Encoding utf8
    Write-Host "   wrote $($kept.Count) line(s) -> $DestPath"
}

# Status (informational; always expect dry_run=True going into Stage 1)
Write-Host ">> host status"
& fly ssh console -a $App -C "python ops/c1_rail_arm.py --status" 2>&1 |
    ForEach-Object { "$_" } |
    Where-Object { $_ -notmatch "Error: The handle is invalid" -and $_ -notmatch "^Connecting to " }

Invoke-FlyDump `
    -RemoteCmd "cat /data/c1_rail_events.jsonl" `
    -DestPath (Join-Path $OutDir "c1_rail_events.jsonl") `
    -Filter { $_.StartsWith("{") }

Invoke-FlyDump `
    -RemoteCmd "cat /data/c1_rail_audit.log" `
    -DestPath (Join-Path $OutDir "c1_rail_audit.log") `
    -Filter { $_ -notmatch "Error: The handle is invalid" -and $_ -notmatch "^Connecting to " }

Write-Host ""
Write-Host "Next:"
Write-Host "  python scripts/m1_item5_capture.py `"$OutDir\c1_rail_events.jsonl`" --preflight --audit-log `"$OutDir\c1_rail_audit.log`""
Write-Host "  python scripts/m1_item5_capture.py `"$OutDir\c1_rail_events.jsonl`" --latest"
