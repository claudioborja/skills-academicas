#!/usr/bin/env python3
"""Conversión, segmentación y protección en Linux, Windows y macOS."""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys

from runtime_portable import configure_console, run_script, select_python

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'editor-en-jefe/scripts'))
from archivos_seguros import validate_outputs


def main() -> int:
    configure_console()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', nargs='?', type=Path)
    parser.add_argument('--max-words', type=int, default=900)
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    source = args.input.expanduser().resolve()
    if not source.is_file():
        parser.error(f'No existe el archivo: {source}')
    if not 100 <= args.max_words <= 10000:
        parser.error('--max-words debe estar entre 100 y 10000.')
    output = (args.output or source.with_name(source.stem + '-preprocesado')).expanduser().resolve()
    stem = source.stem
    names = [f'{stem}{suffix}.{ext}' for suffix in ('', '-segmentos', '-protegidos') for ext in ('md', 'json')]
    if any((output / name).resolve() == source for name in names):
        parser.error('El directorio de salida sobrescribiría el archivo de entrada.')
    try:
        validate_outputs([source], [output/name for name in names], args.overwrite)
        python = select_python(prepare=source.suffix.lower() in {'.pdf', '.docx'})
        output.mkdir(parents=True, exist_ok=True)
        scripts = Path(__file__).resolve().parent
        converted = output / f'{stem}.md'
        steps = [
            ('documento_a_markdown.py', source, '', []),
            ('segmentar_manuscrito.py', converted, '-segmentos', ['--max-words', str(args.max_words)]),
            ('proteger_bloques.py', converted, '-protegidos', []),
        ]
        for script, input_path, suffix, extra in steps:
            result = run_script(python, scripts / script, [str(input_path),
                                '--out', str(output / f'{stem}{suffix}.md'),
                                '--json-out', str(output / f'{stem}{suffix}.json'), *extra,
                                *(['--overwrite'] if args.overwrite else [])])
            if result:
                return result
        print(f'Preprocesamiento completado: {output}')
        return 0
    except subprocess.CalledProcessError as exc:
        return exc.returncode
    except (OSError, RuntimeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
