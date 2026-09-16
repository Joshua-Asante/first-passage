# PowerShell 7.3+ preserves empty arguments and embedded quotes in native argv.
# Bootstrap needs only Python's standard library; fp.py selects the task venv.
# Keep the bootstrap isolated from inherited PYTHONHOME/PYTHONPATH as well.
#Requires -Version 7.3
$PSNativeCommandArgumentPassing = 'Standard'
$PSNativeCommandUseErrorActionPreference = $false
$ErrorActionPreference = 'Stop'
$bootstrap = Get-Command python -CommandType Application -ErrorAction Stop | Select-Object -First 1
& $bootstrap.Source -I "$PSScriptRoot/scripts/fp.py" @args
exit $LASTEXITCODE
