#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'editor-en-jefe/scripts'))
from archivos_seguros import atomic_write, validate_outputs


CHECKS = {
    "titulo": re.compile(r"(?m)^#\s+.+"),
    "resumen": re.compile(r"(?im)^#{1,6}\s+(resumen|abstract)\b"),
    "palabras_clave": re.compile(r"(?i)\b(palabras clave|keywords)\b"),
    "introduccion": re.compile(r"(?im)^#{1,6}\s+introducci[oó]n\b"),
    "metodos": re.compile(r"(?im)^#{1,6}\s+(m[eé]todos?|metodolog[ií]a)\b"),
    "resultados": re.compile(r"(?im)^#{1,6}\s+resultados\b"),
    "discusion": re.compile(r"(?im)^#{1,6}\s+discusi[oó]n\b"),
    "conclusiones": re.compile(r"(?im)^#{1,6}\s+conclusiones?\b"),
    "referencias": re.compile(r"(?im)^#{1,6}\s+(referencias|bibliograf[ií]a|references)\b"),
    "limitaciones": re.compile(r"(?i)\blimitaci[oó]n|limitaciones|limitations?\b"),
    "conflicto_interes": re.compile(r"(?i)\b(conflicto de inter[eé]s|conflicts? of interest)\b"),
}


def run(text: str) -> list[dict]:
    result = []
    for key, pattern in CHECKS.items():
        ok = bool(pattern.search(text))
        severity = "alta" if key in {"resumen", "introduccion", "metodos", "resultados", "discusion", "referencias"} and not ok else "media"
        result.append({"check": key, "ok": ok, "severity": "baja" if ok else severity})
    return result


def render(items: list[dict], source: str) -> str:
    lines = ["# Checklist de envío a revista", "", f"- Fuente: `{source}`", "", "| Ítem | Estado | Severidad |", "| --- | --- | --- |"]
    for item in items:
        lines.append(f"| {item['check']} | {'ok' if item['ok'] else 'revisar'} | {item['severity']} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Checklist mecánico de envío de artículo científico.")
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
    items = run(path.read_text(encoding="utf-8", errors="replace"))
    report = render(items, str(path))
    if args.out:
        atomic_write(args.out, report, overwrite=args.overwrite)
    else:
        sys.stdout.write(report)
    if args.json_out:
        atomic_write(args.json_out, json.dumps(items, ensure_ascii=False, indent=2), overwrite=args.overwrite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
