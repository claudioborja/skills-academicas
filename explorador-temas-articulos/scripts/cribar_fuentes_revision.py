#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import re
import sys
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'editor-en-jefe/scripts'))
from archivos_seguros import atomic_write, validate_outputs
from typing import Any

from common import DOI_RE, compact, read_records, write_csv, write_json


def norm_text(value: Any) -> str:
    text = str(value or "").lower()
    text = re.sub(r"[^a-z0-9áéíóúüñ]+", " ", text, flags=re.I)
    return re.sub(r"\s+", " ", text).strip()


def split_terms(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip().lower() for item in re.split(r"[;,]\s*", value) if item.strip()]


def yes(value: Any) -> bool:
    low = str(value or "").strip().lower()
    return low in {"1", "si", "sí", "yes", "true", "full", "open", "acceso", "pdf"}


def get(row: dict[str, Any], *keys: str) -> str:
    for key in keys:
        if row.get(key):
            return str(row.get(key))
    return ""


def record_key(row: dict[str, Any]) -> tuple[str, str]:
    doi = get(row, "doi", "DOI").strip().lower().rstrip(".,;)")
    title = norm_text(get(row, "title", "titulo", "name"))
    if doi:
        return ("doi", doi)
    return ("title", title)


def deduplicate(records: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    seen: dict[tuple[str, str], int] = {}
    unique = []
    duplicates = []
    for idx, row in enumerate(records, start=1):
        key = record_key(row)
        enriched = dict(row)
        enriched["source_row"] = idx
        if key[1] and key in seen:
            enriched["duplicate_of"] = seen[key]
            duplicates.append(enriched)
            continue
        seen[key] = idx
        unique.append(enriched)
    return unique, duplicates


def decide(row: dict[str, Any], args: argparse.Namespace) -> tuple[str, str]:
    title = get(row, "title", "titulo", "name")
    abstract = get(row, "abstract", "resumen", "summary", "findings")
    text = norm_text(" ".join([title, abstract, get(row, "keywords", "palabras_clave"), get(row, "method")]))
    include_terms = split_terms(args.include_terms)
    exclude_terms = split_terms(args.exclude_terms)
    reasons = []

    if args.year_min or args.year_max:
        year_text = get(row, "year", "ano", "año", "date")
        match = re.search(r"(19|20)\d{2}", year_text)
        year = int(match.group(0)) if match else None
        if year is None:
            reasons.append("sin anio verificable")
        if args.year_min and year is not None and year < args.year_min:
            reasons.append(f"anio menor que {args.year_min}")
        if args.year_max and year is not None and year > args.year_max:
            reasons.append(f"anio mayor que {args.year_max}")

    doi = get(row, "doi")
    if args.require_doi and not DOI_RE.search(doi):
        reasons.append("sin DOI verificable")

    full_text = get(row, "full_text", "full_text_access", "texto_completo", "access", "pdf")
    if args.require_full_text and not yes(full_text):
        reasons.append("sin texto completo confirmado")

    risk = norm_text(get(row, "editorial_risk", "risk", "reputacion", "decision"))
    if args.exclude_red and ("rojo" in risk or "red" in risk):
        reasons.append("fuente con alerta editorial roja")

    if exclude_terms:
        hits = [term for term in exclude_terms if term in text]
        if hits:
            reasons.append("terminos de exclusion: " + ", ".join(hits[:5]))

    if include_terms:
        hits = [term for term in include_terms if term in text]
        if not hits:
            reasons.append("no contiene terminos de inclusion")

    if reasons:
        return "excluir", "; ".join(reasons)
    return "incluir_titulo_resumen", "cumple criterios automaticos iniciales"


def screen(records: list[dict[str, Any]], args: argparse.Namespace) -> dict[str, Any]:
    unique, duplicates = deduplicate(records)
    screened = []
    for idx, row in enumerate(unique, start=1):
        decision, reason = decide(row, args)
        enriched = dict(row)
        enriched.update(
            {
                "screen_id": f"scr-{idx:04d}",
                "decision": decision,
                "exclusion_reason": "" if decision.startswith("incluir") else reason,
                "screening_reason": reason,
            }
        )
        screened.append(enriched)

    counts = collections.Counter(row["decision"] for row in screened)
    prisma = {
        "identified": len(records),
        "duplicates_removed": len(duplicates),
        "screened_title_abstract": len(screened),
        "excluded_title_abstract": counts.get("excluir", 0),
        "eligible_for_full_text": counts.get("incluir_titulo_resumen", 0),
        "included": counts.get("incluir_titulo_resumen", 0),
    }
    return {"screened": screened, "duplicates": duplicates, "prisma_counts": prisma}


def render(payload: dict[str, Any], source: str) -> str:
    counts = payload["prisma_counts"]
    screened = payload["screened"]
    duplicates = payload["duplicates"]
    reason_counts = collections.Counter(row.get("exclusion_reason", "") for row in screened if row.get("decision") == "excluir")
    lines = [
        "# Cribado de fuentes para revision",
        "",
        f"- Fuente: `{source}`",
        f"- Registros identificados: {counts['identified']}",
        f"- Duplicados removidos: {counts['duplicates_removed']}",
        f"- Registros cribados por titulo/resumen: {counts['screened_title_abstract']}",
        f"- Excluidos por titulo/resumen: {counts['excluded_title_abstract']}",
        f"- Elegibles para texto completo: {counts['eligible_for_full_text']}",
        "",
        "## Razones de exclusion",
        "",
    ]
    if reason_counts:
        lines.extend(f"- {reason or 'sin razon'}: {count}" for reason, count in reason_counts.most_common())
    else:
        lines.append("- Sin exclusiones automaticas.")
    lines.extend(["", "## Matriz de cribado", "", "| ID | Decision | Razon | Titulo | DOI |", "| --- | --- | --- | --- | --- |"])
    for row in screened:
        title = compact(get(row, "title", "titulo", "name"), 110).replace("|", "\\|")
        reason = compact(row.get("screening_reason", ""), 90).replace("|", "\\|")
        lines.append(f"| {row.get('screen_id','')} | {row.get('decision','')} | {reason} | {title} | {row.get('doi','')} |")
    if duplicates:
        lines.extend(["", "## Duplicados", "", "| Fila | Duplicado de | Titulo | DOI |", "| --- | --- | --- | --- |"])
        for row in duplicates:
            title = compact(get(row, "title", "titulo", "name"), 110).replace("|", "\\|")
            lines.append(f"| {row.get('source_row','')} | {row.get('duplicate_of','')} | {title} | {row.get('doi','')} |")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Deduplica y criba registros para revision con conteos tipo PRISMA.")
    parser.add_argument("input", help="CSV, JSON, Markdown o TXT con registros.")
    parser.add_argument("--include-terms", help="Terminos obligatorios separados por ; o ,")
    parser.add_argument("--exclude-terms", help="Terminos de exclusion separados por ; o ,")
    parser.add_argument("--year-min", type=int)
    parser.add_argument("--year-max", type=int)
    parser.add_argument("--require-doi", action="store_true")
    parser.add_argument("--require-full-text", action="store_true")
    parser.add_argument("--exclude-red", action="store_true")
    parser.add_argument("--out")
    parser.add_argument("--json-out")
    parser.add_argument("--csv-out")
    parser.add_argument('--overwrite', action='store_true', help='Reemplazar informes existentes, nunca entradas')
    args = parser.parse_args()
    try:
        validate_outputs([args.input], [args.out, args.json_out, args.csv_out], args.overwrite)
    except ValueError as exc:
        parser.error(str(exc))

    payload = screen(read_records(args.input), args)
    report = render(payload, args.input)
    if args.out:
        atomic_write(args.out, report, overwrite=args.overwrite)
    else:
        sys.stdout.write(report)
    if args.json_out:
        write_json(args.json_out, payload, overwrite=args.overwrite)
    if args.csv_out:
        write_csv(args.csv_out, payload["screened"], overwrite=args.overwrite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
