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

if ($power -in 'VM deallocated', 'VM deallocating') {
    Set-AutomationVariable -Name $seenVar -Value 'none'
    "OK: $power (cpu points=$($points.Count))"
    return
}

# Start time: the earlier of the last provisioning operation and the first check
# that saw the VM allocated, so a later operation cannot extend the cap.
$seen = Get-AutomationVariable -Name $seenVar
if ($seen -eq 'none') { $seen = $now.ToString('o'); Set-AutomationVariable -Name $seenVar -Value $seen }
$start = @([datetimeoffset]::Parse($seen)) + @($provisioned | Where-Object { $_ } | ForEach-Object { [datetimeoffset]$_ }) |
    Sort-Object | Select-Object -First 1
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
