#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


MARKERS = {
    "institucional": [
        "trabajo presentado",
        "optar al",
        "optar por",
        "universidad",
        "facultad",
        "tutor",
        "tribunal",
        "jurado",
        "requisito",
    ],
    "estructura_tesis": [
        "planteamiento del problema",
        "marco teórico",
        "marco teorico",
        "metodología",
        "metodologia",
        "resultados",
        "discusión",
        "discusion",
        "conclusiones y recomendaciones",
        "objetivo general",
        "objetivos específicos",
        "objetivos especificos",
        "hipótesis",
        "hipotesis",
        "justificación",
        "justificacion",
    ],
    "metodologia": [
        "población",
        "poblacion",
        "muestra",
        "instrumento",
        "variables",
        "enfoque cuantitativo",
        "enfoque cualitativo",
        "diseño metodológico",
        "diseno metodologico",
        "validez",
        "confiabilidad",
    ],
    "defensa": [
        "la presente investigación",
        "la presente investigacion",
        "se cumplió",
        "se cumplio",
        "se justifica",
        "los resultados obtenidos",
        "permitió comprobar",
        "permitio comprobar",
        "en cumplimiento",
    ],
}


def read_text(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def source_format(path: str) -> str:
    if path == "-":
        return "stdin"
    suffix = Path(path).suffix.lower()
    if suffix in {".md", ".markdown"}:
        return "markdown"
    if suffix == ".txt":
        return "text"
    return "plain-text"


def headings(text: str) -> list[tuple[int, str]]:
    return [
        (line_number, match.group(2).strip())
        for line_number, line in enumerate(text.splitlines(), start=1)
        if (match := re.match(r"^(#{1,6})\s+(.+)$", line))
    ]


def section_at_line(items: list[tuple[int, str]], line_number: int) -> str | None:
    section = None
    for heading_line, title in items:
        if heading_line > line_number:
            break
        section = title
    return section


def find_markers(text: str, items: list[tuple[int, str]]) -> list[dict[str, object]]:
    findings = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        low = line.lower()
        for category, markers in MARKERS.items():
            for marker in markers:
                if re.search(rf"(?<!\w){re.escape(marker)}(?!\w)", low):
                    findings.append(
                        {
                            "category": category,
                            "marker": marker,
                            "line": line_number,
                            "section": section_at_line(items, line_number),
                            "excerpt": line.strip(),
                        }
                    )
    return findings


def count_markers(findings: list[dict[str, object]]) -> dict[str, list[dict[str, object]]]:
    result: dict[str, list[dict[str, object]]] = {}
    for category, markers in MARKERS.items():
        hits: list[dict[str, object]] = []
        for marker in markers:
            count = sum(
                1
                for finding in findings
                if finding["category"] == category and finding["marker"] == marker
            )
            if count:
                hits.append({"marker": marker, "count": count})
        result[category] = sorted(hits, key=lambda h: (-int(h["count"]), str(h["marker"])))
    return result


def chapter_like_headings(items: list[tuple[int, str]]) -> list[dict[str, object]]:
    patterns = [
        r"cap[ií]tulo\s+[ivx\d]+",
        r"planteamiento",
        r"marco te[oó]rico",
        r"metodolog[ií]a",
        r"resultados",
        r"conclusiones",
    ]
    out = []
    for line_number, title in items:
        low = title.lower()
        if any(re.search(p, low) for p in patterns):
            out.append({"line": line_number, "title": title})
    return out


def recommendation(markers: dict[str, list[dict[str, object]]]) -> list[str]:
    recs = []
    if markers["institucional"]:
        recs.append("Eliminar o mover marcas institucionales a agradecimientos o nota editorial.")
    if markers["estructura_tesis"]:
        recs.append("Rediseñar el índice por progresión de lectura, no por capítulos metodológicos.")
    if markers["metodologia"]:
        recs.append("Reducir metodología al cuerpo solo si sostiene credibilidad; si interrumpe, mover a anexo.")
    if markers["defensa"]:
        recs.append("Reescribir lenguaje de defensa como valor para el lector y aporte editorial.")
    if not recs:
        recs.append("No se detectan marcas fuertes de tesis; revisar manualmente estructura y propósito editorial.")
    return recs


def main() -> int:
    parser = argparse.ArgumentParser(description="Diagnostica marcas de tesis para conversión a libro.")
    parser.add_argument("input", help="Archivo UTF-8 o '-' para stdin")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    text = read_text(args.input)
    hs = headings(text)
    findings = find_markers(text, hs)
    markers = count_markers(findings)
    result = {
        "source": {"path": args.input, "format": source_format(args.input)},
        "headings_count": len(hs),
        "chapter_like_headings": chapter_like_headings(hs),
        "markers": markers,
        "findings": findings,
        "recommendations": recommendation(markers),
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    print("Diagnóstico tesis -> libro")
    print("==========================")
    print(f"Encabezados detectados: {result['headings_count']}")
    print()
    print("Encabezados con forma de tesis:")
    for item in result["chapter_like_headings"][:30]:
        print(f"- L{item['line']}: {item['title']}")
    if not result["chapter_like_headings"]:
        print("- Sin hallazgos relevantes")
    print()
    print("Marcadores:")
    for category, hits in markers.items():
        print(f"- {category}:")
        if hits:
            for hit in hits[:12]:
                print(f"  - {hit['count']}x {hit['marker']}")
        else:
            print("  - Sin hallazgos")
    print()
    print("Hallazgos localizables:")
    for finding in findings[:30]:
        section = f" [{finding['section']}]" if finding["section"] else ""
        print(f"- L{finding['line']}{section}: {finding['marker']} — {finding['excerpt']}")
    if not findings:
        print("- Sin hallazgos")
    print()
    print("Recomendaciones:")
    for rec in result["recommendations"]:
        print(f"- {rec}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
