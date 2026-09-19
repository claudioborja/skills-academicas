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


DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.I)
NUM_REF_RE = re.compile(r"^\s*\[(\d+)\]\s*(.+)$")
YEAR_RE = re.compile(r"\b(19|20)\d{2}[a-z]?\b")


@dataclass
class Reference:
    id: str
    original: str
    normalized: str
    style_guess: str
    doi: str
    year: str
    duplicate: bool


def collect_refs(text: str) -> list[str]:
    lines = [line.strip() for line in text.splitlines()]
    refs: list[str] = []
    buffer = ""
    for line in lines:
        if not line:
            if buffer:
                refs.append(buffer.strip())
                buffer = ""
            continue
        if NUM_REF_RE.match(line) or re.match(r"^[A-ZÁÉÍÓÚÑ][\wÁÉÍÓÚÜÑáéíóúüñ' -]+,\s", line):
            if buffer:
                refs.append(buffer.strip())
            buffer = line
        elif buffer:
            buffer += " " + line
    if buffer:
        refs.append(buffer.strip())
    return refs


def normalize(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    value = re.sub(r"\s+([.,;:])", r"\1", value)
    return value


def process(text: str) -> list[Reference]:
    refs = collect_refs(text)
    seen: set[str] = set()
    result: list[Reference] = []
    for idx, ref in enumerate(refs, start=1):
        norm = normalize(ref)
        num = NUM_REF_RE.match(norm)
        style = "ieee" if num else "apa_probable" if YEAR_RE.search(norm) else "desconocido"
        doi_match = DOI_RE.search(norm)
        year_match = YEAR_RE.search(norm)
        doi = doi_match.group(0).rstrip(".,;)").lower() if doi_match else ''
        key = 'doi:' + doi if doi else 'text:' + (num.group(2) if num else norm).casefold()
        duplicate = key in seen
        seen.add(key)
        result.append(
            Reference(
                id=num.group(1) if num else str(idx),
                original=ref,
                normalized=norm,
                style_guess=style,
                doi=doi_match.group(0).rstrip(".,;)").lower() if doi_match else "",
                year=year_match.group(0) if year_match else "",
                duplicate=duplicate,
            )
        )
    return result


def render(refs: list[Reference], source: str) -> str:
    lines = ["# Normalización preliminar de referencias", "", f"- Fuente: `{source}`", f"- Referencias detectadas: {len(refs)}", "", "| ID | Estilo | Año | DOI | Duplicada | Referencia normalizada |", "| --- | --- | --- | --- | --- | --- |"]
    for ref in refs:
        lines.append(f"| {ref.id} | {ref.style_guess} | {ref.year or 'pendiente'} | {ref.doi or 'No detectado'} | {str(ref.duplicate).lower()} | {ref.normalized.replace('|', '\\|')} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Normaliza bibliografía preliminar y detecta DOI/duplicados.")
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
    refs = process(path.read_text(encoding="utf-8", errors="replace"))
    report = render(refs, str(path))
    if args.out:
        atomic_write(args.out, report, overwrite=args.overwrite)
    else:
        sys.stdout.write(report)
    if args.json_out:
        atomic_write(args.json_out, json.dumps([asdict(r) for r in refs], ensure_ascii=False, indent=2), overwrite=args.overwrite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
