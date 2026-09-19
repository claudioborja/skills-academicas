#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'workflow-maestro-academico-editorial/scripts'))
from archivos_seguros import atomic_write, validate_outputs


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.M)
WORD_RE = re.compile(r"\b\w+\b", re.UNICODE)
TABLE_RE = re.compile(r"(?m)^\|.+\|\n\|(?:\s*:?-+:?\s*\|)+\n(?:\|.+\|\n?)+")
FIG_RE = re.compile(r"(?im)\b(figura|fig\.|gráfico|grafico|imagen)\s+\d+")
NUM_CITE_RE = re.compile(r"\[(?:\d+(?:\s*[-,]\s*\d+)*)\]")
APA_CITE_RE = re.compile(r"\([A-ZÁÉÍÓÚÑ][A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+,\s*(?:19|20)\d{2}[a-z]?\)")
REF_HEAD_RE = re.compile(r"(?im)^#{1,6}\s+(referencias|bibliograf[ií]a|references)\s*$")


@dataclass
class Section:
    level: int
    title: str
    start_line: int
    end_line: int
    words: int
    chars: int


def line_at(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def sections(text: str) -> list[Section]:
    matches = list(HEADING_RE.finditer(text))
    result: list[Section] = []
    for idx, match in enumerate(matches):
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        result.append(Section(len(match.group(1)), match.group(2).strip(), line_at(text, start), line_at(text, end), len(WORD_RE.findall(body)), len(body)))
    return result


def render(payload: dict) -> str:
    lines = ["# Inventario documental", "", f"- Fuente: `{payload['source']}`", f"- Palabras: {payload['words']}", f"- Secciones: {len(payload['sections'])}", f"- Tablas Markdown: {payload['tables']}", f"- Figuras mencionadas: {payload['figures']}", f"- Citas numéricas: {payload['numeric_citations']}", f"- Citas APA probables: {payload['apa_citations']}", f"- Bibliografía detectada: {str(payload['bibliography_detected']).lower()}", "", "| Nivel | Título | Líneas | Palabras |", "| --- | --- | --- | --- |"]
    for sec in payload["sections"]:
        title = sec["title"].replace("|", "\\|")
        lines.append(f"| {sec['level']} | {title} | {sec['start_line']}-{sec['end_line']} | {sec['words']} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventaria estructura general de un manuscrito Markdown/TXT.")
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
    text = path.read_text(encoding="utf-8", errors="replace")
    payload = {
        "source": str(path),
        "chars": len(text),
        "words": len(WORD_RE.findall(text)),
        "sections": [asdict(s) for s in sections(text)],
        "tables": len(TABLE_RE.findall(text)),
        "figures": len(FIG_RE.findall(text)),
        "numeric_citations": len(NUM_CITE_RE.findall(text)),
        "apa_citations": len(APA_CITE_RE.findall(text)),
        "bibliography_detected": bool(REF_HEAD_RE.search(text)),
    }
    report = render(payload)
    if args.out:
        atomic_write(args.out, report, overwrite=args.overwrite)
    else:
        sys.stdout.write(report)
    if args.json_out:
        atomic_write(args.json_out, json.dumps(payload, ensure_ascii=False, indent=2), overwrite=args.overwrite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
