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


DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.I)
TEXT_EXT = {".txt", ".md", ".markdown", ".html", ".htm", ".json", ".csv"}


@dataclass
class SourceItem:
    path: str
    extension: str
    bytes: int
    doi: str
    decision: str
    reason: str


def iter_files(path: Path, recursive: bool) -> list[Path]:
    if path.is_file():
        return [path]
    pattern = "**/*" if recursive else "*"
    return [item for item in path.glob(pattern) if item.is_file()]


def sniff_doi(path: Path) -> str:
    if path.suffix.lower() in TEXT_EXT:
        text = path.read_text(encoding="utf-8", errors="replace")[:200000]
        match = DOI_RE.search(text)
        if match:
            return match.group(0).rstrip(".,;)").lower()
    match = DOI_RE.search(path.name.replace("_", "/"))
    return match.group(0).rstrip(".,;)").lower() if match else ""


def inventory(path: Path, recursive: bool) -> list[SourceItem]:
    items: list[SourceItem] = []
    for file in sorted(iter_files(path, recursive)):
        doi = sniff_doi(file)
        decision = "pendiente"
        reason = "Requiere lectura y verificación"
        if not doi:
            reason = "Sin DOI detectado automáticamente"
        items.append(SourceItem(str(file), file.suffix.lower(), file.stat().st_size, doi, decision, reason))
    return items


def render(items: list[SourceItem], source: str) -> str:
    lines = ["# Inventario de fuentes", "", f"- Fuente: `{source}`", f"- Archivos: {len(items)}", "", "| Archivo | Ext | Bytes | DOI | Decisión | Razón |", "| --- | --- | --- | --- | --- | --- |"]
    for item in items:
        lines.append(f"| {item.path.replace('|', '\\|')} | {item.extension} | {item.bytes} | {item.doi or 'No detectado'} | {item.decision} | {item.reason} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventaria fuentes descargadas y DOI probables.")
    parser.add_argument("input")
    parser.add_argument("--recursive", action="store_true")
    parser.add_argument("--out")
    parser.add_argument("--json-out")
    parser.add_argument('--overwrite', action='store_true', help='Reemplazar informes existentes, nunca entradas')
    args = parser.parse_args()
    try:
        validate_outputs(iter_files(Path(args.input), args.recursive), [args.out, args.json_out], args.overwrite)
    except ValueError as exc:
        parser.error(str(exc))
    items = inventory(Path(args.input), args.recursive)
    report = render(items, args.input)
    if args.out:
        atomic_write(args.out, report, overwrite=args.overwrite)
    else:
        sys.stdout.write(report)
    if args.json_out:
        atomic_write(args.json_out, json.dumps([asdict(i) for i in items], ensure_ascii=False, indent=2), overwrite=args.overwrite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
