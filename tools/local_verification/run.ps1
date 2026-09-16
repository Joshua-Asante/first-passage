#requires -Version 7.3
param(
    [string]$EvidencePath,
    [switch]$Build,
    [ValidateRange(0, 8)][int]$Workers = 0,
    [string[]]$TestPath = @('tests/ops/test_book_takeover_phases.py', 'tests/ops/test_book_account_owner.py', 'tests/ops/test_four_leg_runtime.py', 'tests/ops/test_book_close_reconciliation.py', 'tests/ops/test_book_close_review_edges.py', 'tests/ops/test_book_runtime_chronology.py', 'tests/ops/test_book_runtime_close_feedback.py', 'tests/test_record_verification.py', 'tests/sequence_verification/book_event_sequences.py')
)
$ErrorActionPreference = 'Stop'
$PSNativeCommandArgumentPassing = 'Standard'
$PSNativeCommandUseErrorActionPreference = $false
$repo = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
if (-not $EvidencePath) {
    $identity = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ') + '-' + [guid]::NewGuid().ToString('N')
    $EvidencePath = Join-Path $repo ".cache/fp-docker-verification/$identity"
}
$EvidencePath = [IO.Path]::GetFullPath($EvidencePath)
$metadataPath = $EvidencePath + '.environment.json'
if ((Test-Path -LiteralPath $EvidencePath) -or (Test-Path -LiteralPath $metadataPath)) { throw 'Choose a new evidence path; prior evidence is preserved.' }
$dockerCommand = Get-Command docker -ErrorAction SilentlyContinue
$docker = if ($dockerCommand) { $dockerCommand.Source } else { Join-Path $env:LOCALAPPDATA 'Programs/DockerDesktop/resources/bin/docker.exe' }
if (-not (Test-Path -LiteralPath $docker)) { throw 'Docker CLI not found. Install/start Docker Desktop or put docker on PATH.' }
$python = (Get-Command python -ErrorAction Stop | Select-Object -First 1).Source
$oldPath = $env:PATH
try {
    $env:PATH = (Split-Path $docker) + [IO.Path]::PathSeparator + $oldPath
    & $docker version --format '{{.Server.Version}}'
    if ($LASTEXITCODE -ne 0) { throw 'Docker engine is unavailable.' }
    if ($Build) {
        $context = Join-Path (Split-Path $EvidencePath) ('build-' + [guid]::NewGuid().ToString('N'))
        New-Item -ItemType Directory -Path $context -Force | Out-Null
        Copy-Item -LiteralPath (Join-Path $repo 'requirements-ops.lock') -Destination $context
        Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'Dockerfile') -Destination $context
        Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'requirements-extra.txt') -Destination $context
        & $docker build -t first-passage-verification:py311 $context
        if ($LASTEXITCODE -ne 0) { throw 'Verification image build failed.' }
    }
    $image = & $docker image inspect first-passage-verification:py311 --format '{{.Id}}'
    if ($LASTEXITCODE -ne 0) { throw 'Build the image with -Build first.' }
    $runtimeCode = 'import json,sys,platform,re,hashlib,importlib.metadata as m; p={d.metadata["Name"]:d.version for d in m.distributions()}; lock=open("/build/requirements-ops.lock","rb").read(); extra=open("/build/requirements-extra.txt","rb").read(); r=re.findall(r"^([\w.-]+)==([^\s\\]+)",lock.decode(),re.M); errors=[n for n,v in r if m.version(n)!=v]; print(json.dumps(dict(python=sys.version,platform=platform.platform(),packages=p,locked_count=len(r),lock_mismatches=errors,lock_sha256=hashlib.sha256(lock).hexdigest(),extra_sha256=hashlib.sha256(extra).hexdigest()))); sys.exit(bool(errors) or not r)'
    $runtime = & $docker run --rm --network none $image python -c $runtimeCode
    if ($LASTEXITCODE -ne 0) { throw 'Image does not satisfy its operations lock.' }
    $runtimeData = $runtime | ConvertFrom-Json
    if ($runtimeData.lock_sha256 -ne (Get-FileHash (Join-Path $repo 'requirements-ops.lock')).Hash -or $runtimeData.extra_sha256 -ne (Get-FileHash (Join-Path $PSScriptRoot 'requirements-extra.txt')).Hash) { throw 'Image dependency files differ from this checkout. Rebuild with -Build.' }
    New-Item -ItemType Directory -Path (Split-Path $metadataPath) -Force | Out-Null
    @{image_id=$image; runtime=$runtimeData; workers=$Workers; base_image='python:3.11-slim-bookworm@sha256:528257d48c1da0dcecc2e725d1ae34498d60c965f1241e39cd6a85a8859bdf84'} | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $metadataPath
    $dockerArgs = @($docker, 'run', '--rm', '--network', 'none', '--mount', "type=bind,source=$repo,target=/repo,readonly", '--mount', "type=bind,source=$EvidencePath,target=/evidence", '--tmpfs', '/tmp:exec,size=2g', '--env', 'COVERAGE_FILE=/evidence/.coverage', $image, 'python', '-m', 'pytest')
    $dockerArgs += $TestPath
    $dockerArgs += @('-n', "$Workers")
    if ($Workers -gt 0) { $dockerArgs += '--dist=loadscope' }
    $dockerArgs += @('-q', '-p', 'no:cacheprovider', '--tb=short', '--hypothesis-show-statistics', '--basetemp=/tmp/pytest', '--junitxml=/evidence/junit.xml', '--cov=c1_rail.book_account_owner', '--cov=c1_rail.book_takeover_owner', '--cov=c1_signal_daemon.book_runtime', '--cov-branch', '--cov-report=json:/evidence/coverage.json')
    & $python -I (Join-Path $repo 'scripts/record_verification.py') --repo $repo --output $EvidencePath --allow-ignored-output --metadata $metadataPath -- @dockerArgs
    $verificationExit = $LASTEXITCODE
} finally {
    $env:PATH = $oldPath
}
exit $verificationExit
