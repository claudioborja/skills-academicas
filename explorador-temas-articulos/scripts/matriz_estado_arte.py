#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import sys
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'editor-en-jefe/scripts'))
from archivos_seguros import atomic_write, validate_outputs

from common import compact, read_records, write_csv, write_json


def infer_gap(rows: list[dict]) -> str:
    types = {str(row.get("article_type", "")) for row in rows}
    text = " ".join(str(row.get("abstract", "")) for row in rows).lower()
    gaps = []
    if "revision" in types and "original" not in types:
        gaps.append("Predominan revisiones; oportunidad para estudio empírico original.")
    if "original" in types and "revision" not in types and len(rows) >= 4:
        gaps.append("Hay varios estudios originales; oportunidad para revisión integradora.")
    if "ethic" in text or "ética" in text or "privacy" in text or "privacidad" in text:
        gaps.append("La dimensión ética/privacidad aparece como eje transversal.")
    if not gaps:
        gaps.append("Vacío no concluyente; requiere lectura completa y contraste bibliográfico.")
    return " ".join(gaps)


def matrix(records: list[dict]) -> list[dict]:
    groups: dict[str, list[dict]] = collections.defaultdict(list)
    for row in records:
        groups[str(row.get("topic") or "tema_no_detectado")].append(row)
    result = []
    for topic, rows in sorted(groups.items(), key=lambda item: (-len(item[1]), item[0])):
        years = [str(r.get("year", "")) for r in rows if str(r.get("year", "")).strip()]
        result.append(
            {
                "topic": topic,
                "count": len(rows),
                "years": ", ".join(sorted(set(years))),
                "types": ", ".join(f"{k}:{v}" for k, v in collections.Counter(str(r.get("article_type", "no_clasificado")) for r in rows).most_common()),
                "sources": "; ".join(compact(r.get("title", ""), 90) for r in rows[:5]),
                "probable_gap": infer_gap(rows),
            }
        )
    return result


def render(rows: list[dict]) -> str:
    lines = ["# Matriz de estado del arte", "", f"- Grupos temáticos: {len(rows)}", "", "| Tema | N | Años | Tipos | Vacío probable | Fuentes base |", "| --- | --- | --- | --- | --- | --- |"]
    for row in rows:
        lines.append(
            f"| {row['topic'].replace('|', '\\|')} | {row['count']} | {row['years']} | {row['types']} | "
            f"{row['probable_gap'].replace('|', '\\|')} | {row['sources'].replace('|', '\\|')} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Agrupa literatura en matriz de estado del arte.")
    parser.add_argument("input")
    parser.add_argument("--out")
    parser.add_argument("--json-out")
    parser.add_argument("--csv-out")
    parser.add_argument('--overwrite', action='store_true', help='Reemplazar informes existentes, nunca entradas')
    args = parser.parse_args()
    try:
        validate_outputs([args.input], [args.out, args.json_out, args.csv_out], args.overwrite)
    except ValueError as exc:
        parser.error(str(exc))
    rows = matrix(read_records(args.input))
    report = render(rows)
    if args.out:
        atomic_write(args.out, report, overwrite=args.overwrite)
    else:
        sys.stdout.write(report)
    if args.json_out:
        write_json(args.json_out, rows, overwrite=args.overwrite)
    if args.csv_out:
        write_csv(args.csv_out, rows, overwrite=args.overwrite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
