#!/usr/bin/env python3
"""Audita señales editoriales básicas de bloques de código Markdown."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "editor-en-jefe/scripts"))
from archivos_seguros import atomic_write, validate_outputs


FENCE_RE = re.compile(r"^\s*```\s*([^\s`]*)\s*$")
LISTING_TITLE_RE = re.compile(
    r"(?:^|\*\*)(?:listado|c[oó]digo|algoritmo|programa|ejemplo)\s+\d+(?:\.\d+)*\b",
    re.IGNORECASE,
)
WORKING_MARKER_RE = re.compile(r"\b(?:TODO|FIXME|pendiente\s+de\s+(?:editar|revisar|completar))\b", re.IGNORECASE)


def _title_before(lines: list[str], fence_index: int) -> bool:
    """Return whether the preceding visible paragraph is a numbered listing title."""
    index = fence_index - 1
    while index >= 0 and not lines[index].strip():
        index -= 1
    return index >= 0 and bool(LISTING_TITLE_RE.search(lines[index].strip()))


def audit(text: str) -> list[dict]:
    lines = text.splitlines()
    open_block: dict | None = None
    blocks: list[dict] = []

    for number, line in enumerate(lines, start=1):
        fence = FENCE_RE.match(line)
        if fence:
            if open_block is None:
                open_block = {
                    "line": number,
                    "language": fence.group(1),
                    "has_title": _title_before(lines, number - 1),
                    "markers": [],
                }
            else:
                blocks.append(open_block)
                open_block = None
            continue
        if open_block is not None and WORKING_MARKER_RE.search(line):
            open_block["markers"].append(number)

    unclosed = [open_block["line"]] if open_block is not None else []
    no_language = [block["line"] for block in blocks if not block["language"]]
    no_title = [block["line"] for block in blocks if not block["has_title"]]
    markers = [line for block in blocks for line in block["markers"]]
    if open_block is not None:
        markers.extend(open_block["markers"])

    checks = [
        ("bloques_sin_lenguaje", no_language, "alta"),
        ("bloques_sin_titulo", no_title, "media"),
        ("marcadores_de_trabajo", markers, "alta"),
        ("bloques_sin_cierre", unclosed, "alta"),
    ]
    return [
        {"check": name, "ok": not found, "severity": "baja" if not found else severity, "details": {"lines": found}}
        for name, found, severity in checks
    ]


def render(results: list[dict], source: str) -> str:
    lines = ["# Auditoría de listados de código", "", f"- Fuente: `{source}`", "", "| Revisión | Estado | Severidad | Líneas |", "| --- | --- | --- | --- |"]
    for item in results:
        found = ", ".join(map(str, item["details"]["lines"])) or "—"
        lines.append(f"| {item['check']} | {'ok' if item['ok'] else 'revisar'} | {item['severity']} | {found} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Audita bloques de código para publicación técnica.")
    parser.add_argument("input", help="Manuscrito Markdown")
    parser.add_argument("--out", help="Informe Markdown")
    parser.add_argument("--json-out", help="Informe JSON")
    parser.add_argument("--overwrite", action="store_true", help="Autorizar reemplazo de informes, nunca de la entrada")
    args = parser.parse_args()
    try:
        validate_outputs([args.input], [args.out, args.json_out], args.overwrite)
    except ValueError as exc:
        parser.error(str(exc))
    source = Path(args.input)
    results = audit(source.read_text(encoding="utf-8", errors="replace"))
    report = render(results, str(source))
    if args.out:
        atomic_write(args.out, report, overwrite=args.overwrite)
    else:
        sys.stdout.write(report)
    if args.json_out:
        atomic_write(args.json_out, json.dumps(results, ensure_ascii=False, indent=2), overwrite=args.overwrite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
