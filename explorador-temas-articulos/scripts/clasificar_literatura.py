#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import sys
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'editor-en-jefe/scripts'))
from archivos_seguros import atomic_write, validate_outputs

from common import compact, read_records, tokens, write_csv, write_json


TYPE_RULES = [
    ("revision", ["systematic review", "scoping review", "meta-analysis", "meta analysis", "literature review", "review", "prisma", "synthesis"]),
    ("original", ["participants", "sample", "dataset", "survey", "interview", "experiment", "regression", "model trained", "muestra", "participantes", "encuesta", "entrevista", "experimento", "resultados"]),
    ("metodologico", ["framework", "method", "instrument", "validation", "protocol", "modelo", "instrumento", "validación", "metodología"]),
    ("caso", ["case study", "implementation", "intervention", "experiencia", "estudio de caso", "implementación"]),
    ("teorico", ["conceptual", "theoretical", "critical", "teórico", "conceptual"]),
]


def classify_type(text: str) -> tuple[str, str]:
    low = text.lower()
    scores = []
    for kind, clues in TYPE_RULES:
        score = sum(1 for clue in clues if clue in low)
        if score:
            scores.append((score, kind))
    if not scores:
        return "no_clasificado", "Sin señales suficientes"
    score, kind = sorted(scores, reverse=True)[0]
    return kind, f"{score} señal(es) heurística(s)"


def topic_label(text: str, max_terms: int = 3) -> str:
    counts = collections.Counter(tokens(text))
    if not counts:
        return "tema_no_detectado"
    return " / ".join(term for term, _ in counts.most_common(max_terms))


def classify(records: list[dict]) -> list[dict]:
    result = []
    for idx, row in enumerate(records, start=1):
        title = str(row.get("title") or row.get("titulo") or row.get("name") or f"Documento {idx}")
        abstract = str(row.get("abstract") or row.get("resumen") or row.get("summary") or "")
        keywords = str(row.get("keywords") or row.get("palabras_clave") or "")
        source_text = " ".join([title, abstract, keywords, str(row.get("source", "")), str(row.get("method", ""))])
        kind, reason = classify_type(source_text)
        enriched = dict(row)
        enriched.update(
            {
                "id": row.get("id") or f"doc-{idx:03d}",
                "title": title,
                "abstract": abstract,
                "topic": topic_label(source_text),
                "article_type": kind,
                "classification_reason": reason,
            }
        )
        result.append(enriched)
    return result


def render(rows: list[dict]) -> str:
    counts = collections.Counter(row["article_type"] for row in rows)
    topics = collections.Counter(row["topic"] for row in rows)
    lines = ["# Clasificación de literatura", "", f"- Registros: {len(rows)}", ""]
    lines.append("## Tipos")
    lines.extend(f"- `{k}`: {v}" for k, v in counts.most_common())
    lines.extend(["", "## Temas frecuentes"])
    lines.extend(f"- {k}: {v}" for k, v in topics.most_common(12))
    lines.extend(["", "| ID | Año | Tipo | Tema | Título | DOI |", "| --- | --- | --- | --- | --- | --- |"])
    for row in rows:
        lines.append(
            f"| {row.get('id','')} | {row.get('year','')} | {row.get('article_type','')} | {row.get('topic','')} | "
            f"{compact(row.get('title','')).replace('|', '\\|')} | {row.get('doi','')} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Clasifica literatura por tipo y tema probable.")
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
    rows = classify(read_records(args.input))
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
