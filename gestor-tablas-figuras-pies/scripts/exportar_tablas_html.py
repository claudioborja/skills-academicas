#!/usr/bin/env python3
"""Exportar tablas Markdown a una página HTML con índice y anclas."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'editor-en-jefe/scripts'))
from archivos_seguros import atomic_write, validate_outputs


SEPARATOR_RE = re.compile(r"^\s*\|?(?:\s*:?-{3,}:?\s*\|)+\s*$")
CAPTION_RE = re.compile(r"^\s*(?:\*\*)?(Tabla\s+[A-Za-z0-9.-]+[.:\-]?\s*.*?)(?:\*\*)?\s*$", re.I)


def split_row(line: str) -> list[str]:
    value = line.strip().strip("|")
    return [re.sub(r"[*_`]", "", html.unescape(cell.strip())) for cell in value.split("|")]


def extract_tables(text: str) -> list[dict[str, object]]:
    lines = text.splitlines()
    tables: list[dict[str, object]] = []
    index = 0
    while index + 1 < len(lines):
        if "|" not in lines[index] or not SEPARATOR_RE.match(lines[index + 1]):
            index += 1
            continue
        raw_rows = [lines[index]]
        cursor = index + 2
        while cursor < len(lines) and "|" in lines[cursor] and lines[cursor].strip():
            raw_rows.append(lines[cursor])
            cursor += 1
        caption_cursor = index - 1
        while caption_cursor >= 0 and not lines[caption_cursor].strip():
            caption_cursor -= 1
        previous = lines[caption_cursor].strip() if caption_cursor >= 0 else ""
        match = CAPTION_RE.match(previous)
        number = len(tables) + 1
        title = match.group(1) if match else f"Tabla {number}"
        tables.append({"id": f"tabla-{number}", "title": title, "rows": [split_row(row) for row in raw_rows]})
        index = cursor
    return tables


def render(tables: list[dict[str, object]], source: Path) -> str:
    index_items = "\n".join(
        f'<li><a href="#{item["id"]}">{html.escape(str(item["title"]))}</a></li>' for item in tables
    )
    blocks: list[str] = []
    for item in tables:
        rows = item["rows"]
        assert isinstance(rows, list)
        head = rows[0] if rows else []
        body = rows[1:] if len(rows) > 1 else []
        head_html = "".join(f"<th>{html.escape(str(cell))}</th>" for cell in head)
        body_html = "\n".join(
            "<tr>" + "".join(f"<td>{html.escape(str(cell))}</td>" for cell in row) + "</tr>" for row in body
        )
        blocks.append(
            f'<section id="{item["id"]}"><h2>{html.escape(str(item["title"]))}</h2>'
            f'<p class="link"><a href="#{item["id"]}">Enlace permanente a esta tabla</a></p>'
            f'<table><thead><tr>{head_html}</tr></thead><tbody>{body_html}</tbody></table></section>'
        )
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>Tablas del libro</title>
<style>body{{font-family:Arial,sans-serif;max-width:1100px;margin:2rem auto;line-height:1.4}}table{{border-collapse:collapse;width:100%;margin-bottom:3rem}}th,td{{border:1px solid #777;padding:.5rem;vertical-align:top}}th{{background:#e9eef3}}section{{scroll-margin-top:1rem}}.link{{font-size:.9rem}}</style></head>
<body><h1>Tablas del libro</h1><p>Fuente: {html.escape(str(source))}</p><ol>{index_items}</ol>{''.join(blocks)}</body></html>"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument('--overwrite', action='store_true', help='Reemplazar informes existentes, nunca entradas')
    args = parser.parse_args()
    try:
        validate_outputs([args.source], [args.out], args.overwrite)
    except ValueError as exc:
        parser.error(str(exc))
    if not args.source.is_file():
        parser.error(f"No existe el archivo: {args.source}")
    tables = extract_tables(args.source.read_text(encoding="utf-8"))
    atomic_write(args.out, render(tables, args.source.resolve()), overwrite=args.overwrite)
    print(f"Tablas exportadas: {len(tables)}; salida: {args.out}")


if __name__ == "__main__":
    main()
