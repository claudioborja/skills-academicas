#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'editor-en-jefe/scripts'))
from archivos_seguros import atomic_write, validate_outputs


FENCE_RE = re.compile(r"```(?:[^\n]*)\n(.*?)```", re.S)
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
LINK_RE = re.compile(r"!?\[([^\]]*)\]\(([^)]+)\)")
REF_LINK_RE = re.compile(r"\[([^\]]+)\]\[[^\]]+\]")
INLINE_CODE_RE = re.compile(r"`([^`]+)`")
EMPHASIS_RE = re.compile(r"(\*\*|__|\*|_)(.*?)\1")
HEADING_RE = re.compile(r"^(#{1,6})\s*(.*?)\s*#*\s*$")
HR_RE = re.compile(r"^\s{0,3}([-*_])(?:\s*\1){2,}\s*$")
TABLE_ALIGN_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$")


def clean_inline(text: str) -> str:
    text = HTML_COMMENT_RE.sub("", text)
    text = LINK_RE.sub(lambda m: f"{m.group(1)} ({m.group(2)})" if m.group(2).strip() else m.group(1), text)
    text = REF_LINK_RE.sub(r"\1", text)
    text = INLINE_CODE_RE.sub(r"\1", text)
    previous = None
    while previous != text:
        previous = text
        text = EMPHASIS_RE.sub(r"\2", text)
    text = text.replace("\\|", "|")
    text = text.replace("\\*", "*").replace("\\_", "_").replace("\\#", "#")
    return re.sub(r"[ \t]+", " ", text).strip()


def is_table_row(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and stripped.endswith("|") and stripped.count("|") >= 2


def split_table_row(line: str) -> list[str]:
    stripped = line.strip().strip("|")
    return [clean_inline(cell.strip()) for cell in stripped.split("|")]


def render_table(rows: list[list[str]]) -> list[str]:
    if not rows:
        return []
    cleaned = [row for row in rows if any(cell for cell in row)]
    if not cleaned:
        return []
    width = max(len(row) for row in cleaned)
    cleaned = [row + [""] * (width - len(row)) for row in cleaned]
    col_widths = [max(len(row[idx]) for row in cleaned) for idx in range(width)]
    rendered = []
    for row in cleaned:
        rendered.append("  ".join(cell.ljust(col_widths[idx]) for idx, cell in enumerate(row)).rstrip())
    return rendered


def flush_table(table_rows: list[list[str]], output: list[str]) -> None:
    if not table_rows:
        return
    if output and output[-1] != "":
        output.append("")
    output.extend(render_table(table_rows))
    output.append("")
    table_rows.clear()


def convert_markdown_to_txt(markdown: str) -> str:
    markdown = markdown.replace("\r\n", "\n").replace("\r", "\n")
    markdown = FENCE_RE.sub(lambda m: "\n" + m.group(1).strip("\n") + "\n", markdown)
    output: list[str] = []
    table_rows: list[list[str]] = []

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if TABLE_ALIGN_RE.match(stripped):
            continue
        if is_table_row(stripped):
            table_rows.append(split_table_row(stripped))
            continue
        flush_table(table_rows, output)

        if not stripped:
            if output and output[-1] != "":
                output.append("")
            continue

        heading = HEADING_RE.match(stripped)
        if heading:
            if output and output[-1] != "":
                output.append("")
            output.append(clean_inline(heading.group(2)))
            output.append("")
            continue

        if HR_RE.match(stripped):
            if output and output[-1] != "":
                output.append("")
            continue

        stripped = re.sub(r"^\s{0,3}>\s?", "", stripped)
        stripped = re.sub(r"^\s{0,3}[-+*]\s+", "", stripped)
        stripped = re.sub(r"^\s{0,3}\d+[.)]\s+", "", stripped)
        stripped = re.sub(r"^\s{0,3}- \[[ xX]\]\s+", "", stripped)
        cleaned = clean_inline(stripped)
        if cleaned:
            output.append(cleaned)

    flush_table(table_rows, output)
    text = "\n".join(output)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = "\n".join(line.rstrip() for line in text.splitlines())
    return text.strip() + "\n"


def default_output_path(input_path: Path) -> Path:
    if input_path.name.lower() == "libro_completo.md":
        return input_path.with_name("libro_completo.txt")
    return input_path.with_suffix(".txt")


def main() -> int:
    parser = argparse.ArgumentParser(description="Convierte una entrega Markdown a TXT final sin marcas Markdown.")
    parser.add_argument("input", help="Archivo .md/.markdown de entrada.")
    parser.add_argument("--out", help="Ruta .txt de salida. Si se omite, usa el mismo nombre con extension .txt.")
    parser.add_argument("--keep-md", action="store_true", help="Conserva el Markdown intermedio. Por defecto no lo elimina; esta bandera documenta la decision.")
    parser.add_argument('--overwrite', action='store_true', help='Reemplazar una salida existente, nunca la entrada')
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise SystemExit(f"No existe el archivo: {input_path}")
    output_path = Path(args.out) if args.out else default_output_path(input_path)
    if output_path.suffix.lower() != ".txt":
        raise SystemExit("La salida final debe tener extension .txt")

    try:
        validate_outputs([input_path], [output_path], args.overwrite)
    except ValueError as exc:
        parser.error(str(exc))
    text = convert_markdown_to_txt(input_path.read_text(encoding="utf-8", errors="replace"))
    atomic_write(output_path, text, overwrite=args.overwrite)
    sys.stdout.write(f"TXT final: {output_path}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
