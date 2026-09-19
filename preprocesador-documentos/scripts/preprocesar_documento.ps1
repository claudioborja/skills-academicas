[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$InputPath,
    [Parameter(Position = 1)]
    [string]$OutputDirectory,
    [ValidateRange(100, 10000)]
    [int]$MaxWords = 900
)
$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $InputPath -PathType Leaf)) {
    Write-Error "No existe el archivo: $InputPath"
    exit 2
}
$launcher = Join-Path $PSScriptRoot 'preprocesar_documento.py'
$scriptArguments = @($InputPath)
if ($OutputDirectory) { $scriptArguments += $OutputDirectory }
$scriptArguments += @('--max-words', "$MaxWords")
function Find-CompatiblePython {
    $candidates = @('py', 'python3', 'python')
    if ($env:LOCALAPPDATA) {
        # winget may install Python before the current process receives a new PATH.
        $candidates += (Join-Path $env:LOCALAPPDATA 'Programs\Python\Python312\python.exe')
    }
    foreach ($candidate in $candidates) {
        $command = Get-Command $candidate -CommandType Application -ErrorAction SilentlyContinue
        if (-not $command) { continue }
        $prefix = @()
        if ($candidate -eq 'py') { $prefix = @('-3') }
        try {
            $null = & $command.Source @prefix -c 'import sys; sys.exit(sys.version_info < (3, 10))' 2>$null
            if ($LASTEXITCODE -eq 0) {
                return [PSCustomObject]@{ Executable = $command.Source; Prefix = $prefix }
            }
        }
        catch { continue }
    }
    return $null
}

$pythonCommand = Find-CompatiblePython
if (-not $pythonCommand -and $env:OS -eq 'Windows_NT') {
    $winget = Get-Command winget -CommandType Application -ErrorAction SilentlyContinue
    if (-not $winget) {
        Write-Error 'No hay Python compatible ni winget. Instala Python 3.10 o posterior.'
        exit 1
    }
    Write-Host 'Instalando Python 3.12 para el usuario actual...'
    & $winget.Source install --id Python.Python.3.12 --exact --scope user --accept-package-agreements --accept-source-agreements --silent
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    $pythonCommand = Find-CompatiblePython
}
if (-not $pythonCommand) {
    Write-Error 'No se encontro Python 3.10 o posterior. Instala Python o abre una nueva terminal si acabas de instalarlo.'
    exit 1
}
$prefix = @($pythonCommand.Prefix)
& $pythonCommand.Executable @prefix -X utf8 $launcher @scriptArguments
exit $LASTEXITCODE
