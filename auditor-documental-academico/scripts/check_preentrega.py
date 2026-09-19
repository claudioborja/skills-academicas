#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'workflow-maestro-academico-editorial/scripts'))
from archivos_seguros import atomic_write, validate_outputs

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'automatizador-referencias/scripts'))
from auditar_citas_bibliografia import audit


CHECKS = {
    "introduccion": re.compile(r"(?im)^#{1,6}\s+introducci[oó]n\b"),
    "conclusiones": re.compile(r"(?im)^#{1,6}\s+conclusiones?\b"),
    "referencias": re.compile(r"(?im)^#{1,6}\s+(referencias|bibliograf[ií]a|references)\b"),
    "tablas": re.compile(r"(?m)^\|.+\|\n\|(?:\s*:?-+:?\s*\|)+"),
    "citas": re.compile(r"\[(?:\d+(?:\s*[-,]\s*\d+)*)\]|\([A-ZÁÉÍÓÚÑ][A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+,\s*(?:19|20)\d{2}[a-z]?\)"),
}


def run(text: str) -> list[dict]:
    citations = audit(text)
    has_citations = bool(citations.numeric_citations or citations.apa_citations)
    results = []
    for name, pattern in CHECKS.items():
        ok = has_citations if name == 'citas' else bool(pattern.search(text))
        severity = "media"
        if name == "referencias" and has_citations and not ok:
            severity = "alta"
        results.append({"check": name, "ok": ok, "severity": "baja" if ok else severity})
    return results


def render(results: list[dict], source: str) -> str:
    lines = ["# Checklist mecánico de preentrega", "", f"- Fuente: `{source}`", "", "| Revisión | Estado | Severidad |", "| --- | --- | --- |"]
    for item in results:
        lines.append(f"| {item['check']} | {'ok' if item['ok'] else 'revisar'} | {item['severity']} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Checklist mecánico de preentrega académica.")
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
    results = run(path.read_text(encoding="utf-8", errors="replace"))
    report = render(results, str(path))
    if args.out:
        atomic_write(args.out, report, overwrite=args.overwrite)
    else:
        sys.stdout.write(report)
    if args.json_out:
        atomic_write(args.json_out, json.dumps(results, ensure_ascii=False, indent=2), overwrite=args.overwrite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
