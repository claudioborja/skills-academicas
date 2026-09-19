#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'workflow-maestro-academico-editorial/scripts'))
from archivos_seguros import atomic_write, validate_outputs


PATTERNS = {
    "objetivo": re.compile(r"(?i)(?:objetivo|prop[oó]sito|aim|objective)[^.]{0,240}\."),
    "metodo": re.compile(r"(?i)(?:m[eé]todo|metodolog[ií]a|diseño|muestra|corpus|participantes|analysis|an[aá]lisis)[^.]{0,240}\."),
    "resultado": re.compile(r"(?i)(?:resultado|hallazgo|se encontr[oó]|muestra que|indica que|results?)[^.]{0,240}\."),
    "discusion": re.compile(r"(?i)(?:discusi[oó]n|sugiere|implica|coincide|contrasta|literatura|limitaci[oó]n)[^.]{0,240}\."),
}


def collect(text: str) -> dict[str, list[str]]:
    return {key: [re.sub(r"\s+", " ", m.group(0)).strip() for m in pattern.finditer(text)][:8] for key, pattern in PATTERNS.items()}


def render(payload: dict, source: str) -> str:
    lines = ["# Matriz objetivo-método-resultados-discusión", "", f"- Fuente: `{source}`", "", "| Elemento | Fragmentos detectados |", "| --- | --- |"]
    for key, values in payload.items():
        joined = "<br>".join(v.replace("|", "\\|") for v in values) if values else "No detectado"
        lines.append(f"| {key} | {joined} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Extrae fragmentos para matriz de alineación IMRyD.")
    parser.add_argument("input")
    parser.add_argument("--out")
    parser.add_argument("--json-out")
    parser.add_argument('--overwrite', action='store_true', help='Autorizar reemplazo de informes, nunca de entradas')
    args = parser.parse_args()
    try:
        validate_outputs([args.input], [args.out, args.json_out], args.overwrite)
    except ValueError as exc:
        parser.error(str(exc))
    path = Path(args.input)
    payload = collect(path.read_text(encoding="utf-8", errors="replace"))
    report = render(payload, str(path))
    if args.out:
        atomic_write(args.out, report, overwrite=args.overwrite)
    else:
        sys.stdout.write(report)
    if args.json_out:
        atomic_write(args.json_out, json.dumps(payload, ensure_ascii=False, indent=2), overwrite=args.overwrite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
