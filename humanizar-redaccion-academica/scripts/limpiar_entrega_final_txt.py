#!/usr/bin/env python3
"""Conservar TXT y retirar solo líneas expresamente seleccionadas."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'editor-en-jefe/scripts'))
from archivos_seguros import atomic_write, validate_outputs


def clean_text(text: str, remove_lines=()) -> tuple[str, dict[str, int]]:
    lines = text.splitlines(keepends=True)
    selected = set(remove_lines)
    if any(not isinstance(n, int) or n < 1 or n > len(lines) for n in selected):
        raise ValueError('Número de línea fuera del documento.')
    return ''.join(line for n, line in enumerate(lines, 1) if n not in selected), {
        'guide_lines_removed': len(selected), 'blank_lines_collapsed': 0, 'final_replacements': 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    parser.add_argument('--out', required=True, help='Archivo diferente del original.')
    parser.add_argument('--report')
    parser.add_argument('--remove-lines', type=int, nargs='+', default=[],
                        help='Números de líneas aprobadas para eliminar; sin esta opción no altera contenido.')
    parser.add_argument('--overwrite', action='store_true', help='Reemplazar salidas existentes, nunca la entrada.')
    args = parser.parse_args()
    source, output = Path(args.input), Path(args.out)
    try:
        validate_outputs([source], [output, args.report], args.overwrite)
        original = source.read_bytes().decode('utf-8')
        cleaned, stats = clean_text(original, args.remove_lines)
        atomic_write(output, cleaned, args.overwrite)
        stats.update(input=str(source), output=str(output),
                     original_characters=len(original), final_characters=len(cleaned))
        if args.report:
            atomic_write(args.report, json.dumps(stats, ensure_ascii=False, indent=2), args.overwrite)
        print(json.dumps(stats, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
