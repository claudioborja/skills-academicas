#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'editor-en-jefe/scripts'))
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
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.M)
OPERATIONAL_HEADING_RE = re.compile(
    r"\b(plantilla(?:\s+obligatoria)?|checklist|control(?:es)?\s+de\s+calidad|roles?\s+de\s+trabajo|"
    r"flujo\s+de\s+trabajo|entregables|criterios\s+editoriales|instrucciones\s+para)\b",
    re.I,
)
CHECKBOX_RE = re.compile(r"(?m)^\s*[-*+]\s*\[[ xX]\]\s+")
WORKING_MARKER_RE = re.compile(r"(?im)\b(pendiente\s+de\s+(?:editar|revisar|completar)|insertar\s+(?:figura|tabla)|verificar\s+fuente)\b")


def headings(text: str) -> list[dict]:
    return [
        {"level": len(match.group(1)), "title": match.group(2).strip(), "line": text.count("\n", 0, match.start()) + 1}
        for match in HEADING_RE.finditer(text)
    ]


def normalized_heading(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).casefold()


def structure_check(items: list[dict], expected_headings: list[str] | None) -> list[dict]:
    skipped_levels = []
    duplicates = []
    seen = set()
    previous_level = None
    for item in items:
        if previous_level is not None and item["level"] > previous_level + 1:
            skipped_levels.append({"line": item["line"], "from": previous_level, "to": item["level"]})
        previous_level = item["level"]
        key = normalized_heading(item["title"])
        if key in seen and item["title"] not in duplicates:
            duplicates.append(item["title"])
        seen.add(key)
    results = [{
        "check": "jerarquia_titulos",
        "ok": not skipped_levels and not duplicates,
        "severity": "baja" if not skipped_levels and not duplicates else "media",
        "details": {"skipped_levels": skipped_levels, "duplicates": duplicates},
    }]
    if expected_headings is not None:
        expected = {normalized_heading(title) for title in expected_headings}
        unexpected = [item["title"] for item in items if normalized_heading(item["title"]) not in expected]
        results.append({
            "check": "estructura_autorizada",
            "ok": not unexpected,
            "severity": "baja" if not unexpected else "alta",
            "details": {"unexpected": unexpected},
        })
    return results


def run(text: str, expected_headings: list[str] | None = None) -> list[dict]:
    citations = audit(text)
    has_citations = bool(citations.numeric_citations or citations.apa_citations)
    results = []
    for name, pattern in CHECKS.items():
        ok = has_citations if name == 'citas' else bool(pattern.search(text))
        severity = "media"
        if name == "referencias" and has_citations and not ok:
            severity = "alta"
        results.append({"check": name, "ok": ok, "severity": "baja" if ok else severity})
    items = headings(text)
    operational = [item["title"] for item in items if OPERATIONAL_HEADING_RE.search(item["title"])]
    results.append({
        "check": "rotulos_operativos",
        "ok": not operational,
        "severity": "baja" if not operational else "alta",
        "details": {"headings": operational},
    })
    code_fences = len(re.findall(r"(?m)^\s*```", text))
    checkboxes = len(CHECKBOX_RE.findall(text))
    working_markers = len(WORKING_MARKER_RE.findall(text))
    results.append({
        "check": "marcas_de_trabajo",
        "ok": not (code_fences or checkboxes or working_markers),
        "severity": "baja" if not (code_fences or checkboxes or working_markers) else "alta",
        "details": {"code_fences": code_fences, "checkboxes": checkboxes, "working_markers": working_markers},
    })
    results.extend(structure_check(items, expected_headings))
    return results


def render(results: list[dict], source: str) -> str:
    lines = ["# Checklist mecánico de preentrega", "", f"- Fuente: `{source}`", "", "| Revisión | Estado | Severidad |", "| --- | --- | --- |"]
    for item in results:
        lines.append(f"| {item['check']} | {'ok' if item['ok'] else 'revisar'} | {item['severity']} |")
    details = [item for item in results if not item["ok"] and item.get("details")]
    if details:
        lines.extend(["", "## Detalles para corregir", ""])
        for item in details:
            data = item["details"]
            if item["check"] == "rotulos_operativos":
                lines.append(f"- Rótulos operativos: {', '.join(data['headings'])}.")
            elif item["check"] == "marcas_de_trabajo":
                lines.append(f"- Marcas de trabajo — Cercas: {data['code_fences']}; Casillas: {data['checkboxes']}; Marcadores: {data['working_markers']}.")
            elif item["check"] == "jerarquia_titulos":
                lines.append(f"- Jerarquía — Saltos: {data['skipped_levels']}; Duplicados: {', '.join(data['duplicates']) or 'ninguno'}.")
            elif item["check"] == "estructura_autorizada":
                lines.append(f"- Encabezados fuera de la estructura autorizada: {', '.join(data['unexpected'])}.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Checklist mecánico de preentrega académica.")
    parser.add_argument("input")
    parser.add_argument("--out")
    parser.add_argument("--json-out")
    parser.add_argument("--estructura", help="Índice Markdown/TXT autorizado; compara sus encabezados con el manuscrito")
    parser.add_argument('--overwrite', action='store_true', help='Autorizar reemplazo de informes, nunca de entradas')
    args = parser.parse_args()
    try:
        validate_outputs([args.input, args.estructura], [args.out, args.json_out], args.overwrite)
    except ValueError as exc:
        parser.error(str(exc))
    path = Path(args.input)
    expected_headings = None
    if args.estructura:
        expected_headings = [item["title"] for item in headings(Path(args.estructura).read_text(encoding="utf-8", errors="replace"))]
    results = run(path.read_text(encoding="utf-8", errors="replace"), expected_headings)
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
