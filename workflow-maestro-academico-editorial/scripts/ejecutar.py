#!/usr/bin/env python3
"""Ejecutar las herramientas de esta colección en Linux, Windows o macOS."""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'preprocesador-documentos/scripts'))
from runtime_portable import configure_console, run_script, select_python
from archivos_seguros import validate_cli


def main() -> int:
    configure_console()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preparar', action='store_true', help='Crear entorno local e instalar dependencias PDF/DOCX.')
    parser.add_argument('--permitir-sobrescritura', action='store_true', help='Permitir reemplazar salidas existentes, nunca entradas; colocar antes del script.')
    parser.add_argument('script', nargs='?', help='Ruta absoluta o relativa a este directorio de skills.')
    parser.add_argument('argumentos', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if not args.script and not args.preparar:
        parser.error('Indica un script o usa --preparar.')
    script = None
    if args.script:
        script = Path(args.script)
        if not script.is_absolute():
            script = ROOT / script
        if not script.is_file() or script.suffix != '.py':
            parser.error(f'No existe el script Python: {script}')
    try:
        validate_cli(args.argumentos, overwrite=args.permitir_sobrescritura)
        python = select_python(prepare=args.preparar)
        if script:
            return run_script(python, script, args.argumentos)
        print(f'Entorno preparado: {python}')
        return 0
    except subprocess.CalledProcessError as exc:
        return exc.returncode
    except (OSError, RuntimeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
