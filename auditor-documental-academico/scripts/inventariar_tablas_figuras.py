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


TABLE_RE = re.compile(r"(?m)^\|.+\|\n\|(?:\s*:?-+:?\s*\|)+\n(?:\|.+\|\n?)+")
CAPTION_RE = re.compile(
    r"(?im)^\s*(tabla|figura|gráfico|grafico)\s+(\d+)\s*(?:[:.\-]\s*(.*))?$"
)
NOTE_RE = re.compile(r"(?im)^\s*\*?Nota\.\*?\s*.*$")
WORD_RE = re.compile(r"\b[\wÁÉÍÓÚÜÑáéíóúüñ]+\b", re.UNICODE)
MIN_POST_ANALYSIS_WORDS = 60


@dataclass
class VisualItem:
    kind: str
    number: str
    line: int
    title: str
    called_in_text: bool
    post_analysis_words: int
    post_analysis_ok: bool
    continuity_issue: str


def line_at(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def next_nonempty(lines: list[str], start: int = 0) -> tuple[int, str] | tuple[None, None]:
    for index in range(start, len(lines)):
        if lines[index].strip():
            return index, lines[index].strip()
    return None, None


def is_boundary(line: str) -> bool:
    return bool(
        line.startswith("#")
        or line.startswith("|")
        or line.startswith("![")
        or CAPTION_RE.fullmatch(line)
        or re.match(r"^\d+\.\s+", line)
    )


def title_after_caption(text: str, match: re.Match[str]) -> str:
    inline = (match.group(3) or "").strip()
    if inline:
        return inline
    _, line = next_nonempty(text[match.end():].splitlines())
    if line and line.startswith("*") and line.endswith("*"):
        return line.strip("*").strip()
    return ""


def audit_post_analysis(text: str, match: re.Match[str]) -> tuple[int, bool, str]:
    tail = text[match.end():]
    note = NOTE_RE.search(tail)
    if not note:
        return 0, False, "falta la nota del recurso"

    lines = tail[note.end():].splitlines()
    first_index, first_line = next_nonempty(lines)
    if first_line is None:
        return 0, False, "falta análisis posterior"
    if is_boundary(first_line):
        return 0, False, f"la nota desemboca directamente en `{first_line[:60]}`"

    paragraph_lines: list[str] = []
    for line in lines[first_index:]:
        stripped = line.strip()
        if not stripped:
            break
        if is_boundary(stripped):
            break
        paragraph_lines.append(stripped)
    words = len(WORD_RE.findall(" ".join(paragraph_lines)))
    if words < MIN_POST_ANALYSIS_WORDS:
        return words, False, f"análisis posterior breve ({words} palabras; mínimo mecánico {MIN_POST_ANALYSIS_WORDS})"
    return words, True, ""


def audit(text: str) -> dict:
    captions = []
    for match in CAPTION_RE.finditer(text):
        kind = match.group(1).lower()
        num = match.group(2)
        call_re = re.compile(rf"(?i)\b{re.escape(kind)}\s+{re.escape(num)}\b")
        called_before = bool(call_re.search(text[max(0, match.start() - 4000):match.start()]))
        words, analysis_ok, issue = audit_post_analysis(text, match)
        captions.append(
            VisualItem(
                kind,
                num,
                line_at(text, match.start()),
                title_after_caption(text, match),
                called_before,
                words,
                analysis_ok,
                issue,
            )
        )
    tables = [{"line": line_at(text, m.start()), "chars": m.end() - m.start()} for m in TABLE_RE.finditer(text)]
    issues = [
        f"{item.kind.title()} {item.number}: {item.continuity_issue}"
        for item in captions
        if not item.post_analysis_ok
    ]
    return {"captions": [asdict(c) for c in captions], "markdown_tables": tables, "continuity_issues": issues}


def render(payload: dict, source: str) -> str:
    lines = ["# Inventario de tablas y figuras", "", f"- Fuente: `{source}`", f"- Títulos detectados: {len(payload['captions'])}", f"- Tablas Markdown: {len(payload['markdown_tables'])}", f"- Fallas de continuidad: {len(payload['continuity_issues'])}", "", "| Tipo | Nº | Línea | Llamada previa | Análisis posterior | Palabras | Título |", "| --- | --- | --- | --- | --- | ---: | --- |"]
    for item in payload["captions"]:
        lines.append(f"| {item['kind']} | {item['number']} | {item['line']} | {str(item['called_in_text']).lower()} | {str(item['post_analysis_ok']).lower()} | {item['post_analysis_words']} | {item['title'].replace('|', '\\|')} |")
    if payload["continuity_issues"]:
        lines.extend(["", "## Fallas de continuidad", ""])
        lines.extend(f"- {issue}" for issue in payload["continuity_issues"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventaria tablas, figuras y llamadas en texto.")
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
    payload = audit(path.read_text(encoding="utf-8", errors="replace"))
    report = render(payload, str(path))
    if args.out:
        atomic_write(args.out, report, overwrite=args.overwrite)
    else:
        sys.stdout.write(report)
    if args.json_out:
        atomic_write(args.json_out, json.dumps(payload, ensure_ascii=False, indent=2), overwrite=args.overwrite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
