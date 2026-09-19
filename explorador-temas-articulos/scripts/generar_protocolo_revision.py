#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'workflow-maestro-academico-editorial/scripts'))
from archivos_seguros import atomic_write, validate_outputs
from typing import Any

from common import write_json


DEFAULT_DATABASES = ["Scopus", "Web of Science", "PubMed", "IEEE Xplore", "SciELO", "Redalyc", "DOAJ"]


def split_terms(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in re.split(r"[;,]\s*", value) if item.strip()]


def quote(term: str) -> str:
    term = term.strip()
    if not term:
        return ""
    if " " in term and not (term.startswith('"') and term.endswith('"')):
        return f'"{term}"'
    return term


def boolean_group(terms: list[str]) -> str:
    cleaned = [quote(term) for term in terms if term.strip()]
    if not cleaned:
        return ""
    if len(cleaned) == 1:
        return cleaned[0]
    return "(" + " OR ".join(cleaned) + ")"


def build_search_strings(concepts: list[str], contexts: list[str], methods: list[str], years: str) -> dict[str, str]:
    groups = [boolean_group(group) for group in (concepts, contexts, methods) if group]
    base = " AND ".join(group for group in groups if group)
    if not base:
        base = boolean_group(concepts) or "<conceptos principales>"
    strings = {}
    for db in DEFAULT_DATABASES:
        if db in {"Scopus", "Web of Science"}:
            query = f"TITLE-ABS-KEY({base})" if db == "Scopus" else f"TS=({base})"
        elif db == "PubMed":
            query = f"({base})"
        elif db == "IEEE Xplore":
            query = f'("{base}")' if " AND " not in base else base
        else:
            query = base
        if years:
            query = f"{query} ; years: {years}"
        strings[db] = query
    return strings


def methodology_defaults(methodology: str) -> tuple[str, list[str]]:
    key = methodology.lower().replace("-", "_")
    if key in {"prisma", "revision", "revision_sistematica", "systematic_review"}:
        return "PRISMA 2020", ["PICO/PICOS", "PECO"]
    if key in {"scoping", "scoping_review", "prisma_scr", "alcance"}:
        return "PRISMA-ScR", ["PCC"]
    if key in {"metaanalisis", "meta_analysis"}:
        return "PRISMA 2020 + plan estadistico", ["PICO/PICOS"]
    if key in {"cualitativo", "qualitative"}:
        return "COREQ/SRQR", ["SPIDER"]
    return methodology or "Revision narrativa/integrativa con criterios explicitos", ["Pregunta conceptual"]


def build_protocol(args: argparse.Namespace) -> dict[str, Any]:
    concepts = split_terms(args.concepts) or split_terms(args.topic)
    contexts = split_terms(args.contexts)
    methods = split_terms(args.methods)
    databases = split_terms(args.databases) or DEFAULT_DATABASES
    guide, frameworks = methodology_defaults(args.methodology)
    years = args.years or "sin restriccion inicial"
    languages = split_terms(args.languages) or ["espanol", "ingles"]
    strings = build_search_strings(concepts, contexts, methods, years if years != "sin restriccion inicial" else "")
    strings = {db: strings.get(db, " AND ".join(filter(None, [boolean_group(concepts), boolean_group(contexts), boolean_group(methods)]))) for db in databases}
    return {
        "topic": args.topic,
        "question": args.question,
        "review_type": args.methodology,
        "reporting_guide": guide,
        "question_framework_options": frameworks,
        "databases": databases,
        "search_date": args.search_date,
        "years": years,
        "languages": languages,
        "document_types": split_terms(args.document_types) or ["articulos revisados por pares", "revisiones sistematicas", "metaanalisis"],
        "concept_terms": concepts,
        "context_terms": contexts,
        "method_terms": methods,
        "inclusion_criteria": split_terms(args.include) or [
            "pertinencia directa con la pregunta",
            "texto completo accesible",
            "metadatos verificables",
            "fuente sin alerta editorial roja",
        ],
        "exclusion_criteria": split_terms(args.exclude) or [
            "sin texto completo",
            "sin DOI o metadatos verificables cuando el area lo exige",
            "fuente editorial en alerta roja",
            "no responde a la pregunta de revision",
        ],
        "search_strings": strings,
        "screening_outputs": [
            "matriz de registros brutos",
            "matriz deduplicada",
            "matriz de cribado con decision y razon",
            "conteos tipo PRISMA",
        ],
    }


def render(protocol: dict[str, Any]) -> str:
    lines = [
        "# Protocolo de busqueda para revision",
        "",
        f"- Tema: {protocol['topic']}",
        f"- Pregunta: {protocol['question'] or 'pendiente de afinar'}",
        f"- Tipo de revision: {protocol['review_type']}",
        f"- Guia de reporte: {protocol['reporting_guide']}",
        f"- Marcos de pregunta sugeridos: {', '.join(protocol['question_framework_options'])}",
        f"- Fecha de busqueda: {protocol['search_date']}",
        f"- Rango temporal: {protocol['years']}",
        f"- Idiomas: {', '.join(protocol['languages'])}",
        "",
        "## Bases de datos",
        "",
    ]
    lines.extend(f"- {db}" for db in protocol["databases"])
    lines.extend(["", "## Cadenas de busqueda", ""])
    for db, query in protocol["search_strings"].items():
        lines.extend([f"### {db}", "", f"```text\n{query}\n```", ""])
    lines.extend(["## Criterios de inclusion", ""])
    lines.extend(f"- {item}" for item in protocol["inclusion_criteria"])
    lines.extend(["", "## Criterios de exclusion", ""])
    lines.extend(f"- {item}" for item in protocol["exclusion_criteria"])
    lines.extend(["", "## Evidencias de trazabilidad", ""])
    lines.extend(f"- {item}" for item in protocol["screening_outputs"])
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Genera protocolo y cadenas de busqueda para revisiones.")
    parser.add_argument("--topic", required=True, help="Tema general o concepto principal.")
    parser.add_argument("--question", default="", help="Pregunta de revision.")
    parser.add_argument("--methodology", default="revision_sistematica", help="revision_sistematica, scoping, metaanalisis, narrativa, cualitativo.")
    parser.add_argument("--concepts", help="Terminos principales separados por ; o ,")
    parser.add_argument("--contexts", help="Contextos/poblaciones separados por ; o ,")
    parser.add_argument("--methods", help="Metodos/tipos de estudio separados por ; o ,")
    parser.add_argument("--databases", help="Bases separadas por ; o ,")
    parser.add_argument("--years", help="Ejemplo: 2020-2026")
    parser.add_argument("--languages", help="Idiomas separados por ; o ,")
    parser.add_argument("--document-types", help="Tipos documentales separados por ; o ,")
    parser.add_argument("--include", help="Criterios de inclusion separados por ;")
    parser.add_argument("--exclude", help="Criterios de exclusion separados por ;")
    parser.add_argument("--search-date", default="pendiente de registrar")
    parser.add_argument("--out")
    parser.add_argument("--json-out")
    parser.add_argument('--overwrite', action='store_true', help='Reemplazar informes existentes, nunca entradas')
    args = parser.parse_args()
    try:
        validate_outputs([], [args.out, args.json_out], args.overwrite)
    except ValueError as exc:
        parser.error(str(exc))
    protocol = build_protocol(args)
    report = render(protocol)
    if args.out:
        atomic_write(args.out, report, overwrite=args.overwrite)
    else:
        sys.stdout.write(report)
    if args.json_out:
        write_json(args.json_out, protocol, overwrite=args.overwrite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
