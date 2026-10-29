# Azure Automation runbook (PowerShell 7.2): 4-hourly backstop for the compute VM.
# Policy: docs/governance/azure-compute-vm-policy.md. Deallocates when the VM is
# stopped but still allocated, idle (average CPU under the threshold for the
# window: stuck, or finished and left on), or past the run cap; a busy VM under
# the cap is left running. Reads status and metrics on every run so a missing
# permission fails the job even while the VM is deallocated.
param(
    [string]$ResourceGroup = 'fp-compute-01_group',
    [string]$VmName = 'fp-compute-01',
    [double]$IdleCpuPercent = 5,
    [int]$IdleMinutes = 60,
    [double]$MaxHours = 12
)
$ErrorActionPreference = 'Stop'
$seenVar = 'FirstSeenRunningUtc'  # 'none' while deallocated

Connect-AzAccount -Identity | Out-Null
$now = [datetimeoffset]::UtcNow
$vm = Get-AzVM -ResourceGroupName $ResourceGroup -Name $VmName
$view = Get-AzVM -ResourceGroupName $ResourceGroup -Name $VmName -Status
$power = ($view.Statuses | Where-Object Code -like 'PowerState/*').DisplayStatus
$provisioned = ($view.Statuses | Where-Object Code -like 'ProvisioningState/*').Time
$metric = Get-AzMetric -ResourceId $vm.Id -MetricName 'Percentage CPU' -AggregationType Average `
    -StartTime $now.UtcDateTime.AddMinutes(-$IdleMinutes) -EndTime $now.UtcDateTime -TimeGrain 00:05:00 -WarningAction SilentlyContinue
$points = @($metric.Data | Where-Object { $null -ne $_.Average } | ForEach-Object Average)
$cpu = if ($points.Count) { [math]::Round(($points | Measure-Object -Average).Average, 2) } else { $null }

$lastStart = Get-AzActivityLog -ResourceId $vm.Id -StartTime $now.UtcDateTime.AddHours(-($MaxHours + 5)) -WarningAction SilentlyContinue |
    Where-Object { $_.OperationName.Value -eq 'Microsoft.Compute/virtualMachines/start/action' -and $_.Status.Value -eq 'Succeeded' } |
    ForEach-Object { [datetimeoffset]$_.EventTimestamp } | Sort-Object | Select-Object -Last 1
if ($power -in 'VM deallocated', 'VM deallocating') {
    Set-AutomationVariable -Name $seenVar -Value 'none'
    "OK: $power (cpu points=$($points.Count), last start $lastStart)"
    return
}

# Start time: the last successful start in the activity log, so a deallocate and
# restart between checks begins a new baseline; other operations never move it.
# Without a logged start, the first check that saw the VM allocated (or the last
# provisioning operation, if earlier) is the baseline.
$seen = Get-AutomationVariable -Name $seenVar
$start = if ($seen -ne 'none') { [datetimeoffset]::Parse($seen) }
if ($lastStart -and (-not $start -or $lastStart -gt $start)) { $start = $lastStart }
elseif (-not $start) {
    $start = @($now) + @($provisioned | Where-Object { $_ } | ForEach-Object { [datetimeoffset]$_ }) | Sort-Object | Select-Object -First 1
}
if ($start.ToString('o') -ne $seen) { Set-AutomationVariable -Name $seenVar -Value $start.ToString('o') }
$hours = [math]::Round(($now - $start).TotalHours, 2)

$reason = if ($power -eq 'VM stopped') { 'stopped but still allocated' }
    elseif ($hours -ge $MaxHours) { "running $hours h, cap $MaxHours h" }
    elseif ($hours * 60 -ge $IdleMinutes -and $null -ne $cpu -and $cpu -lt $IdleCpuPercent) { "idle: cpu $cpu% over $IdleMinutes min" }
if (-not $reason) {
    "OK: $power, running $hours h, cpu $cpu%; left running"
    return
}

"DEALLOCATING: $reason"
Stop-AzVM -ResourceGroupName $ResourceGroup -Name $VmName -Force | Out-Null
$after = ((Get-AzVM -ResourceGroupName $ResourceGroup -Name $VmName -Status).Statuses | Where-Object Code -like 'PowerState/*').DisplayStatus
if ($after -ne 'VM deallocated') { throw "deallocation not verified: $after" }
Set-AutomationVariable -Name $seenVar -Value 'none'
"verified: VM deallocated"
