#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
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


def headings(text: str) -> list[str]:
    return re.findall(r"^(#{1,6})\s+(.+)$", text, flags=re.M)


def count_markers(text: str) -> dict[str, list[dict[str, object]]]:
    low = text.lower()
    result = {}
    for category, markers in MARKERS.items():
        hits = []
        for marker in markers:
            count = low.count(marker)
            if count:
                hits.append({"marker": marker, "count": count})
        result[category] = sorted(hits, key=lambda h: (-int(h["count"]), str(h["marker"])))
    return result


def chapter_like_headings(items: list[str]) -> list[str]:
    patterns = [
        r"cap[ií]tulo\s+[ivx\d]+",
        r"planteamiento",
        r"marco te[oó]rico",
        r"metodolog[ií]a",
        r"resultados",
        r"conclusiones",
    ]
    out = []
    for _, title in items:
        low = title.lower()
        if any(re.search(p, low) for p in patterns):
            out.append(title)
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
    markers = count_markers(text)
    result = {
        "headings_count": len(hs),
        "chapter_like_headings": chapter_like_headings(hs),
        "markers": markers,
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
        print(f"- {item}")
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
    print("Recomendaciones:")
    for rec in result["recommendations"]:
        print(f"- {rec}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
