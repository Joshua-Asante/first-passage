# Idempotent deployment of the compute-VM backstop (policy:
# docs/governance/azure-compute-vm-policy.md). Run by, or under the az login of,
# a subscription owner. Creates an Automation account with a system identity, a
# custom role (VM read, deallocate, metrics and activity-log read) assigned on the VM only, the
# runbook, a 4-hourly schedule, then one probe job. Never prints the subscription ID.
param(
    [string]$ResourceGroup = 'fp-compute-01_group',
    [string]$VmName = 'fp-compute-01',
    [string]$Account = 'fp-compute-01-backstop',
    [string]$Location = 'eastus',
    [string]$Az = 'C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd'
)
$ErrorActionPreference = 'Stop'
$api = 'api-version=2023-11-01'
$runbook = 'fp-vm-backstop'
$schedule = 'every-4-hours'
$jobScheduleId = '6f1e2d3c-4b5a-4968-8778-a6b5c4d3e2f1'  # fixed so reruns update, not duplicate
$roleName = 'FP compute VM backstop'

function Invoke-Az { $out = & $Az @args; if ($LASTEXITCODE) { throw "az $($args[0..1] -join ' ') failed" }; $out }
function Arm([string]$Method, [string]$Path, $Body, [string]$ContentType = 'application/json') {
    $file = New-TemporaryFile
    try {
        $text = if ($Body -is [string]) { $Body } else { $Body | ConvertTo-Json -Depth 8 }
        if ($null -ne $Body) { Set-Content -LiteralPath $file -Value $text -NoNewline }
        $a = @('rest', '--method', $Method, '--url', "https://management.azure.com$Path`?$api", '--headers', "Content-Type=$ContentType")
        if ($null -ne $Body) { $a += @('--body', "@$file") }
        $out = Invoke-Az @a
        if ($out) { $out | ConvertFrom-Json }
    } finally { Remove-Item -LiteralPath $file -ErrorAction SilentlyContinue }
}

$sub = Invoke-Az account show --query id -o tsv
$rgId = "/subscriptions/$sub/resourceGroups/$ResourceGroup"
$vmId = "$rgId/providers/Microsoft.Compute/virtualMachines/$VmName"
$acct = "$rgId/providers/Microsoft.Automation/automationAccounts/$Account"

'account'
$a = Arm PUT $acct @{ location = $Location; identity = @{ type = 'SystemAssigned' }
    properties = @{ sku = @{ name = 'Basic' }; disableLocalAuth = $true } }
$principal = $a.identity.principalId

'role'
$role = @{ Name = $roleName; IsCustom = $true
    Description = 'Read status and CPU metrics of the compute VM and deallocate it; nothing else.'
    Actions = @('Microsoft.Compute/virtualMachines/read', 'Microsoft.Compute/virtualMachines/deallocate/action',
                'Microsoft.Insights/metrics/read', 'Microsoft.Insights/metricDefinitions/read',
                'Microsoft.Insights/eventtypes/values/read')
    NotActions = @(); AssignableScopes = @($rgId) }
$roleFile = New-TemporaryFile
try {
    $role | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $roleFile
    $exists = @(Invoke-Az role definition list --custom-role-only true --name $roleName --scope $rgId -o json | ConvertFrom-Json)
    if ($exists.Count) { Invoke-Az role definition update --role-definition "@$roleFile" -o none }
    else { Invoke-Az role definition create --role-definition "@$roleFile" -o none }
} finally { Remove-Item -LiteralPath $roleFile -ErrorAction SilentlyContinue }
for ($i = 0; $i -lt 10; $i++) {  # new role definitions and identities take time to replicate
    $n = @(& $Az role assignment list --assignee $principal --scope $vmId --role $roleName -o json 2>$null | ConvertFrom-Json)
    if ($n.Count) { $LASTEXITCODE = 0; break }
    & $Az role assignment create --assignee-object-id $principal --assignee-principal-type ServicePrincipal --role $roleName --scope $vmId -o none 2>$null
    if (-not $LASTEXITCODE) { break }
    Start-Sleep 30
}
if ($LASTEXITCODE) { throw 'role assignment failed' }

'runbook'
Arm PUT "$acct/variables/FirstSeenRunningUtc" @{ properties = @{ value = '"none"'; isEncrypted = $false } } | Out-Null
Arm PUT "$acct/runbooks/$runbook" @{ location = $Location
    properties = @{ runbookType = 'PowerShell72'; logProgress = $false; logVerbose = $false
        description = 'Deallocates the compute VM when stopped-allocated, idle, or past the run cap.' } } | Out-Null
Arm PUT "$acct/runbooks/$runbook/draft/content" (Get-Content -Raw "$PSScriptRoot/runbook.ps1") 'text/powershell' | Out-Null
Arm POST "$acct/runbooks/$runbook/publish" $null | Out-Null

'schedule'
$startTime = [datetimeoffset]::UtcNow.AddMinutes(15).ToString('yyyy-MM-ddTHH:mm:00Z')
Arm PUT "$acct/schedules/$schedule" @{ properties = @{ startTime = $startTime; frequency = 'Hour'; interval = 4; timeZone = 'UTC' } } | Out-Null
try { Arm DELETE "$acct/jobSchedules/$jobScheduleId" $null | Out-Null } catch { }
$binding = @{ ResourceGroup = $ResourceGroup; VmName = $VmName }  # same VM the role is assigned on
Arm PUT "$acct/jobSchedules/$jobScheduleId" @{ properties = @{ schedule = @{ name = $schedule }; runbook = @{ name = $runbook }; parameters = $binding } } | Out-Null

'probe job'
$job = [guid]::NewGuid().ToString()
Arm PUT "$acct/jobs/$job" @{ properties = @{ runbook = @{ name = $runbook }; parameters = $binding } } | Out-Null
do { Start-Sleep 15; $status = (Arm GET "$acct/jobs/$job" $null).properties.status } while ($status -notin 'Completed', 'Failed', 'Stopped', 'Suspended')
"probe status: $status"
Invoke-Az rest --method GET --url "https://management.azure.com$acct/jobs/$job/output?$api"
if ($status -ne 'Completed') { exit 1 }
