#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'workflow-maestro-academico-editorial/scripts'))
from archivos_seguros import atomic_write, validate_outputs

from common import read_records, write_json


def article_type(types: str, gap: str) -> str:
    low = f"{types} {gap}".lower()
    if "predominan revisiones" in low:
        return "artículo original empírico"
    if "oportunidad para revisión" in low:
        return "revisión narrativa, sistemática o scoping review"
    if "metodologico" in low or "framework" in low:
        return "artículo metodológico"
    return "artículo original o revisión focalizada"


def proposals(rows: list[dict], limit: int) -> list[dict]:
    ranked = sorted(rows, key=lambda r: int(r.get("count") or 0), reverse=True)[:limit]
    result = []
    for idx, row in enumerate(ranked, start=1):
        topic = str(row.get("topic", "tema"))
        gap = str(row.get("probable_gap", "Vacío pendiente de precisar."))
        kind = article_type(str(row.get("types", "")), gap)
        result.append(
            {
                "id": f"tema-{idx:03d}",
                "tentative_title": f"{topic.title()}: oportunidades de investigación desde el estado del arte",
                "recommended_article_type": kind,
                "research_question": f"¿Cómo se configura {topic} en la literatura reciente y qué oportunidad de investigación queda abierta?",
                "justification": gap,
                "base_sources": row.get("sources", ""),
                "needed_data": "Confirmar corpus, criterios de inclusión, fuentes completas y disponibilidad de datos propios si será original.",
                "main_risk": "La propuesta es heurística; requiere lectura completa y verificación bibliográfica antes de formular novedad.",
            }
        )
    return result


def render(items: list[dict]) -> str:
    lines = ["# Propuestas de temas de artículos", "", f"- Propuestas: {len(items)}"]
    for item in items:
        lines.extend(
            [
                "",
                f"## {item['id']}: {item['tentative_title']}",
                "",
                f"- Tipo recomendado: {item['recommended_article_type']}",
                f"- Pregunta: {item['research_question']}",
                f"- Justificación: {item['justification']}",
                f"- Fuentes base: {item['base_sources']}",
                f"- Datos necesarios: {item['needed_data']}",
                f"- Riesgo: {item['main_risk']}",
            ]
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Propone temas de artículos desde una matriz de estado del arte.")
    parser.add_argument("input")
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--out")
    parser.add_argument("--json-out")
    parser.add_argument('--overwrite', action='store_true', help='Reemplazar informes existentes, nunca entradas')
    args = parser.parse_args()
    try:
        validate_outputs([args.input], [args.out, args.json_out], args.overwrite)
    except ValueError as exc:
        parser.error(str(exc))
    items = proposals(read_records(args.input), args.limit)
    report = render(items)
    if args.out:
        atomic_write(args.out, report, overwrite=args.overwrite)
    else:
        sys.stdout.write(report)
    if args.json_out:
        write_json(args.json_out, items, overwrite=args.overwrite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
