# Managed Run Command entry. PowerShell 5.1 compatible; no passwords or primary-checkout copy.
$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$request = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($RequestBase64)) | ConvertFrom-Json
$config = $request.config
$root = [IO.Path]::GetFullPath($config.guest_root)
New-Item -ItemType Directory -Force $root | Out-Null
$job = "$root/jobs/$($request.spec.job_id)"
New-Item -ItemType Directory -Force $job | Out-Null
# Full bootstrap diagnostics remain on the guest; never print instance bindings.
Start-Transcript -LiteralPath "$job/bootstrap.log" -Append | Out-Null
$transcribing = $true
try {
$utf8 = New-Object Text.UTF8Encoding($false)
function Write-JsonAtomic($Path, $Value) {
    $temp = "$Path.tmp"
    [IO.File]::WriteAllText($temp, ($Value | ConvertTo-Json -Depth 20), $utf8)
    Move-Item -LiteralPath $temp -Destination $Path -Force
}
function Invoke-Checked($Executable, $Arguments) {
    if ([DateTimeOffset]::UtcNow.ToUnixTimeSeconds() -ge $config.execution_deadline) { throw "Bootstrap execution cutoff reached" }
    & $Executable @Arguments
    if ($LASTEXITCODE -ne 0) { throw 'Guest setup command failed' }
}
function Signed-Download($Uri, $Path, $Publisher) {
    Invoke-WebRequest -UseBasicParsing -Uri $Uri -OutFile $Path
    $signature = Get-AuthenticodeSignature -LiteralPath $Path
    if ($signature.Status -ne 'Valid' -or $signature.SignerCertificate.Subject -notmatch $Publisher) {
        throw 'Installer signature/publisher validation failed'
    }
}
$pythonDirectory = Join-Path $root 'python'
$python = Join-Path $pythonDirectory 'python.exe'
if (!(Test-Path -LiteralPath $python)) {
    $installer = "$root/python-install.exe"
    Signed-Download 'https://www.python.org/ftp/python/3.13.2/python-3.13.2-amd64.exe' $installer 'Python Software Foundation'
    $installed = Start-Process -FilePath $installer -ArgumentList @('/quiet','/log',"$job/python-install.log",'InstallAllUsers=1',"TargetDir=$pythonDirectory",'Include_test=0','PrependPath=0','Include_launcher=0') -Wait -PassThru -WindowStyle Hidden
    if ($installed.ExitCode -ne 0) {
        $detail = Get-Content -LiteralPath "$job/python-install.log" -Tail 15 -ErrorAction SilentlyContinue | Out-String
        throw "Python install failed, exit=$($installed.ExitCode): $detail"
    }
}
$version = & $python -c 'import sys; print(sys.version.split()[0])'
if ($version -ne '3.13.2') { throw 'Unexpected bootstrap Python version' }
$gitDirectory = Join-Path $root 'git'
$git = Join-Path $gitDirectory 'cmd/git.exe'
if (!(Test-Path -LiteralPath $git)) {
    $installer = "$root/git-install.exe"
    Signed-Download 'https://github.com/git-for-windows/git/releases/download/v2.51.0.windows.1/Git-2.51.0-64-bit.exe' $installer 'Johannes Schindelin|Git Development Community'
    $installed = Start-Process -FilePath $installer -ArgumentList @('/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART','/SP-',"/DIR=$gitDirectory") -Wait -PassThru -WindowStyle Hidden
    if ($installed.ExitCode -ne 0) { throw 'Git install failed' }
}
$env:PATH = "$root/git/cmd;$env:PATH"
$managementPython = "$root/management/Scripts/python.exe"
if (!(Test-Path -LiteralPath $managementPython)) { Invoke-Checked $python @('-m','venv',"$root/management") }
Invoke-Checked $managementPython @('-m','pip','install','--disable-pip-version-check','azure-cli==2.91.0')
$az = "$root/management/Scripts/az.cmd"
[IO.File]::WriteAllText($az, "@echo off`r`n`"$managementPython`" -Im azure.cli %*`r`n", [Text.Encoding]::ASCII)
Invoke-Checked $az @('login','--identity','--only-show-errors','-o','none')
$runner = "$root/runner-$($request.runner_commit)"
if (!(Test-Path -LiteralPath "$runner/.git")) {
    Invoke-Checked $git @('init',$runner)
    Invoke-Checked $git @('-C',$runner,'remote','add','origin',$config.repository)
    Invoke-Checked $git @('-C',$runner,'config','core.autocrlf','false')
    Invoke-Checked $git @('-C',$runner,'fetch','--depth','1','origin',$request.runner_commit)
    Invoke-Checked $git @('-C',$runner,'checkout','--detach','FETCH_HEAD')
}
$actual = & $git -C $runner rev-parse HEAD
$dirty = & $git -C $runner status --porcelain --untracked-files=all
if ($actual -ne $request.runner_commit -or $dirty) { throw 'Refusing unpinned or dirty runner source' }
$config.az = $az
$config.state_dir = "$root/control"
$config | Add-Member -Force python $python
$config | Add-Member -Force git $git
Write-JsonAtomic "$root/config.json" $config
New-Item -ItemType Directory -Force "$root/control/sessions" | Out-Null
Write-JsonAtomic "$root/control/sessions/$($config.session_id).json" @{session_id=$config.session_id;source_job_id=$request.spec.job_id}
$job = "$root/jobs/$($request.spec.job_id)"
New-Item -ItemType Directory -Force $job | Out-Null
Write-JsonAtomic "$job/spec.json" $request.spec
$action = New-ScheduledTaskAction -Execute $python -Argument "-I `"$runner/scripts/azure_jobs/guest_entry.py`" watchdog `"$root/config.json`""
$trigger = New-ScheduledTaskTrigger -AtStartup
$settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Days 7) -RestartCount 999 -RestartInterval (New-TimeSpan -Minutes 1) -StartWhenAvailable
if (Get-ScheduledTask -TaskName 'FirstPassageOfflineWatchdog' -ErrorAction SilentlyContinue) {
    Stop-ScheduledTask -TaskName 'FirstPassageOfflineWatchdog'
}
Register-ScheduledTask -TaskName 'FirstPassageOfflineWatchdog' -Action $action -Trigger $trigger -Settings $settings -User 'SYSTEM' -RunLevel Highest -Force | Out-Null
Start-ScheduledTask -TaskName 'FirstPassageOfflineWatchdog'
Write-JsonAtomic "$root/watchdog-installed.json" @{time=[DateTime]::UtcNow.ToString('o');runner_commit=$request.runner_commit}
Stop-Transcript | Out-Null
$transcribing = $false
Invoke-Checked $python @('-I',"$runner/scripts/azure_jobs/guest_entry.py",$config.mode,"$root/config.json","$job/spec.json")

} finally { if ($transcribing) { Stop-Transcript | Out-Null } }
