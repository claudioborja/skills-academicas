param(
    [Parameter(Position = 0, Mandatory = $true)] [string] $Accion,
    [Parameter(ValueFromRemainingArguments = $true)] [string[]] $Argumentos
)
$raiz = Split-Path -Parent $MyInvocation.MyCommand.Path
$arquitectura = [Environment]::GetEnvironmentVariable('PROCESSOR_ARCHITECTURE')
if ($arquitectura -ne 'AMD64') { throw "Plataforma no empaquetada: Windows $arquitectura" }
$runtime = Join-Path $raiz '../editor-en-jefe/runtime/python'
$python = Join-Path $runtime 'windows-x86_64-py314/python.exe'
$script = switch ($Accion) {
    'generar-listado' {
        & $python -m pip install --disable-pip-version-check --no-index `
            --find-links (Join-Path $runtime 'wheels/windows-x86_64-py314') `
            -r (Join-Path $raiz '../requirements.txt')
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
        Join-Path $raiz 'scripts/generar_listado_docx.py'; break
    }
    'auditar-listados' { Join-Path $raiz 'scripts/auditar_listados_codigo.py'; break }
    default { throw 'Uso: ejecutar.ps1 {generar-listado|auditar-listados} argumentos' }
}
& $python -X utf8 $script @Argumentos
exit $LASTEXITCODE
