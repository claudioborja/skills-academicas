#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'workflow-maestro-academico-editorial/scripts'))
from archivos_seguros import atomic_write, validate_outputs


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.M)
WORD_RE = re.compile(r"\b\w+\b", re.UNICODE)


@dataclass
class Segment:
    id: str
    level: int
    title: str
    start_line: int
    end_line: int
    chars: int
    words: int
    preview: str


def line_number_at(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def preview(text: str, max_chars: int = 360) -> str:
    clean = re.sub(r"\s+", " ", text).strip()
    if len(clean) <= max_chars:
        return clean
    return clean[:max_chars].rsplit(" ", 1)[0] + "..."


def segment_by_headings(text: str) -> list[Segment]:
    matches = list(HEADING_RE.finditer(text))
    if not matches:
        return []
    segments: list[Segment] = []
    for idx, match in enumerate(matches):
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        title = match.group(2).strip()
        segments.append(
            Segment(
                id=f"s{idx + 1:03d}",
                level=len(match.group(1)),
                title=title,
                start_line=line_number_at(text, start),
                end_line=line_number_at(text, end),
                chars=len(body),
                words=len(WORD_RE.findall(body)),
                preview=preview(body),
            )
        )
    return segments


def segment_by_size(text: str, max_words: int) -> list[Segment]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    segments: list[Segment] = []
    current: list[str] = []
    current_words = 0
    start_line = 1
    line_cursor = 1
    for paragraph in paragraphs:
        words = len(WORD_RE.findall(paragraph))
        if current and current_words + words > max_words:
            body = "\n\n".join(current)
            idx = len(segments) + 1
            segments.append(
                Segment(
                    id=f"s{idx:03d}",
                    level=1,
                    title=f"Segmento {idx}",
                    start_line=start_line,
                    end_line=line_cursor,
                    chars=len(body),
                    words=len(WORD_RE.findall(body)),
                    preview=preview(body),
                )
            )
            start_line = line_cursor + 1
            current = []
            current_words = 0
        current.append(paragraph)
        current_words += words
        line_cursor += paragraph.count("\n") + 2
    if current:
        body = "\n\n".join(current)
        idx = len(segments) + 1
        segments.append(
            Segment(
                id=f"s{idx:03d}",
                level=1,
                title=f"Segmento {idx}",
                start_line=start_line,
                end_line=line_cursor,
                chars=len(body),
                words=len(WORD_RE.findall(body)),
                preview=preview(body),
            )
        )
    return segments


def render(segments: list[Segment], source: str) -> str:
    total_words = sum(segment.words for segment in segments)
    lines = [
        "# Segmentación de manuscrito",
        "",
        f"- Fuente: `{source}`",
        f"- Segmentos: {len(segments)}",
        f"- Palabras aproximadas: {total_words}",
        "",
        "| ID | Nivel | Título | Líneas | Palabras | Vista previa |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in segments:
        safe_preview = item.preview.replace("|", "\\|")
        lines.append(
            f"| {item.id} | {item.level} | {item.title.replace('|', '\\|')} | "
            f"{item.start_line}-{item.end_line} | {item.words} | {safe_preview} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Segmenta Markdown por encabezados o por tamaño.")
    parser.add_argument("input", help="Archivo Markdown/TXT")
    parser.add_argument("--out", help="Ruta Markdown de salida")
    parser.add_argument("--json-out", help="Ruta JSON de salida")
    parser.add_argument("--max-words", type=int, default=900, help="Tamaño por segmento si no hay encabezados")
    parser.add_argument('--overwrite', action='store_true', help='Reemplazar informes existentes, nunca entradas')
    args = parser.parse_args()
    try:
        validate_outputs([args.input], [args.out, args.json_out], args.overwrite)
    except ValueError as exc:
        parser.error(str(exc))

    path = Path(args.input)
    text = path.read_text(encoding="utf-8", errors="replace")
    segments = segment_by_headings(text) or segment_by_size(text, args.max_words)
    report = render(segments, str(path))

    if args.out:
        atomic_write(args.out, report, overwrite=args.overwrite)
    else:
        sys.stdout.write(report)

    if args.json_out:
        payload = {"source": str(path), "segments": [asdict(segment) for segment in segments]}
        atomic_write(args.json_out, json.dumps(payload, ensure_ascii=False, indent=2), overwrite=args.overwrite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
