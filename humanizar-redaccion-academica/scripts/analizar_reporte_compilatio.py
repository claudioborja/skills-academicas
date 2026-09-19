#!/usr/bin/env python3
"""Resume reportes PDF de Compilatio/Magister para revisión editorial.

El script no determina plagio ni autoría. Extrae porcentajes visibles,
fuentes de similitud y fragmentos resaltados por color cuando el PDF conserva
las marcas como dibujos. Requiere PyMuPDF: pip install pymupdf.
"""

from __future__ import annotations

import argparse
import collections
import re
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'workflow-maestro-academico-editorial/scripts'))
from archivos_seguros import atomic_write, validate_outputs

try:
    import pymupdf as fitz  # type: ignore
except Exception as exc:  # pragma: no cover
    raise SystemExit("Falta PyMuPDF. Instala con: pip install pymupdf") from exc


COLOR_LABELS = {
    (0.0, 0.749, 1.0): "deteccion_ia",
    (1.0, 0.357, 0.706): "idioma_no_reconocido",
    (0.631, 0.431, 0.416): "texto_entre_comillas_o_bloque",
    (0.863, 0.784, 0.863): "similitud",
    (0.6, 0.2, 0.6): "similitud",
}


def color_key(color):
    if not color:
        return None
    return tuple(round(float(part), 3) for part in color)


def horizontal_overlap(a0, a1, b0, b1):
    return max(0.0, min(a1, b1) - max(a0, b0))


def extract_percentages(first_page_text: str) -> dict[str, str]:
    labels = {
        "Textos sospechosos": "textos_sospechosos",
        "Similitudes": "similitudes",
        "Detección de IA": "deteccion_ia",
        "Idiomas no reconocidos": "idioma_no_reconocido",
        "Textos entre comillas": "textos_entre_comillas",
    }
    lines = [line.strip() for line in first_page_text.splitlines() if line.strip()]
    result: dict[str, str] = {}
    percent_re = re.compile(r"<?\d+%")
    for i, line in enumerate(lines):
        for label, key in labels.items():
            if label in line and key not in result:
                if key == "textos_sospechosos":
                    windows = [
                        lines[max(0, i - 3) : i],
                        lines[i + 1 : min(len(lines), i + 8)],
                    ]
                else:
                    windows = [lines[i + 1 : min(len(lines), i + 12)]]
                for window in windows:
                    for candidate in window:
                        if percent_re.fullmatch(candidate):
                            result[key] = candidate
                            break
                    if key in result:
                        break
    for i, line in enumerate(lines):
        if percent_re.fullmatch(line):
            window = " ".join(lines[max(0, i - 6) : i])
            for label, key in labels.items():
                if label in window and key not in result:
                    result[key] = line
    return result


def extract_sources(page_text: str) -> list[str]:
    lines = [line.strip() for line in page_text.splitlines() if line.strip()]
    sources: list[str] = []
    for line in lines:
        if line.startswith(("www.", "dx.doi.org", "http")):
            continue
        if len(line) > 25 and not re.fullmatch(r"<?\d+%|\d+", line):
            if any(token in line.lower() for token in ("nist", "documento", "guide", "framework", "ciberseguridad", "privacy")):
                sources.append(line)
    return sources[:10]


def extract_highlighted_lines(doc) -> dict[str, list[tuple[int, str]]]:
    grouped: dict[tuple[int, str, int, int], dict[int, tuple[float, str]]] = collections.defaultdict(dict)
    for page_index in range(2, doc.page_count):
        page = doc[page_index]
        words = page.get_text("words")
        for drawing in page.get_drawings():
            key = color_key(drawing.get("fill"))
            label = COLOR_LABELS.get(key)
            if not label:
                continue
            rect = drawing["rect"]
            for word in words:
                x0, y0, x1, y1, text, block, line, word_no = word[:8]
                if horizontal_overlap(x0, x1, rect.x0, rect.x1) <= 0:
                    continue
                if rect.y0 >= y0 - 2 and rect.y0 <= y1 + 5:
                    grouped[(page_index + 1, label, int(block), int(line))][int(word_no)] = (x0, text)

    by_label: dict[str, list[tuple[int, str]]] = collections.defaultdict(list)
    for (page, label, _block, _line), items in sorted(grouped.items()):
        text = " ".join(token for _x, token in sorted(items.values()))
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            by_label[label].append((page, text))
    return by_label


def build_markdown(pdf: Path, doc, percentages, sources, highlights) -> str:
    lines = [
        "# Revisión editorial de reporte Compilatio",
        "",
        f"Archivo: `{pdf.name}`",
        f"Páginas del reporte: {doc.page_count}",
        "",
        "## Indicadores",
        "",
        "| Indicador | Resultado |",
        "|---|---:|",
    ]
    for key, label in [
        ("textos_sospechosos", "Textos sospechosos"),
        ("similitudes", "Similitudes"),
        ("deteccion_ia", "Detección de IA"),
        ("idioma_no_reconocido", "Idiomas no reconocidos"),
        ("textos_entre_comillas", "Textos entre comillas"),
    ]:
        if key in percentages:
            lines.append(f"| {label} | {percentages[key]} |")

    lines.extend(["", "## Fuentes visibles", ""])
    if sources:
        lines.extend(f"- {source}" for source in sources)
    else:
        lines.append("- No se extrajeron fuentes visibles.")

    lines.extend(["", "## Fragmentos por categoría", ""])
    for label, rows in sorted(highlights.items()):
        pages = collections.Counter(page for page, _text in rows)
        word_count = sum(len(text.split()) for _page, text in rows)
        lines.extend([
            f"### {label.replace('_', ' ').title()}",
            "",
            f"- Líneas marcadas: {len(rows)}",
            f"- Palabras aproximadas: {word_count}",
            f"- Páginas principales: {pages.most_common(10)}",
            "",
        ])
        for page, text in rows[:20]:
            lines.append(f"- p. {page}: {text[:240]}")
        lines.append("")

    lines.extend([
        "## Criterio de uso",
        "",
        "Este resumen orienta una revisión editorial. No prueba plagio ni autoría. Si la similitud es baja y la detección IA se concentra en transiciones, introducciones, conclusiones o plantillas, conviene hacer ajustes puntuales y preservar citas, DOI, bibliografía, tablas y diagramas.",
    ])
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument('--overwrite', action='store_true', help='Reemplazar informes existentes, nunca entradas')
    args = parser.parse_args()
    try:
        validate_outputs([args.pdf], [args.out], args.overwrite)
    except ValueError as exc:
        parser.error(str(exc))

    doc = fitz.open(args.pdf)
    first = doc[0].get_text() if doc.page_count else ""
    second = doc[1].get_text() if doc.page_count > 1 else ""
    percentages = extract_percentages(first)
    sources = extract_sources(second)
    highlights = extract_highlighted_lines(doc)
    markdown = build_markdown(args.pdf, doc, percentages, sources, highlights)

    if args.out:
        atomic_write(args.out, markdown, overwrite=args.overwrite)
    else:
        print(markdown)


if __name__ == "__main__":
    main()
