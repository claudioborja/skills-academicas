#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'editor-en-jefe/scripts'))
from archivos_seguros import atomic_write, validate_outputs


PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("doi", re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", re.I)),
    ("url", re.compile(r"https?://[^\s<>)]+", re.I)),
    ("cita_numerica", re.compile(r"\[(?:\d+(?:\s*[-,]\s*\d+)*)\]")),
    ("cita_apa_probable", re.compile(r"\([A-ZÁÉÍÓÚÑ][A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+,\s*(?:19|20)\d{2}[a-z]?(?:,\s*p{1,2}\.\s*\d+)?\)")),
    ("formula", re.compile(r"(?m)^\s*\$\$.*?\$\$\s*$", re.S)),
    ("bloque_cita", re.compile(r"(?m)^(?:>\s?.+(?:\n|$))+")),
    ("bloque_codigo", re.compile(r"```[\s\S]*?```")),
    ("tabla_markdown", re.compile(r"(?m)^\|.+\|\n\|(?:\s*:?-+:?\s*\|)+\n(?:\|.+\|\n?)+")),
    ("referencia_probable", re.compile(r"(?m)^(?:\[\d+\]\s+|[A-ZÁÉÍÓÚÑ][\wÁÉÍÓÚÜÑáéíóúüñ' -]+,\s[A-Z]\.).{30,}$")),
    ("comillas", re.compile(r"“[^”]{20,}”|\"[^\"]{20,}\"")),
]


@dataclass
class ProtectedBlock:
    id: str
    kind: str
    start_line: int
    end_line: int
    chars: int
    text: str


def line_number_at(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def compact(value: str, max_chars: int = 500) -> str:
    clean = re.sub(r"\s+", " ", value).strip()
    if len(clean) <= max_chars:
        return clean
    return clean[:max_chars].rsplit(" ", 1)[0] + "..."


def detect(text: str) -> list[ProtectedBlock]:
    found: list[tuple[int, int, str, str]] = []
    for kind, pattern in PATTERNS:
        for match in pattern.finditer(text):
            found.append((match.start(), match.end(), kind, match.group(0)))
    found.sort(key=lambda item: (item[0], -(item[1] - item[0])))

    selected: list[tuple[int, int, str, str]] = []
    occupied: list[tuple[int, int]] = []
    for start, end, kind, value in found:
        if any(not (end <= a or start >= b) for a, b in occupied):
            continue
        selected.append((start, end, kind, value))
        occupied.append((start, end))

    blocks: list[ProtectedBlock] = []
    for idx, (start, end, kind, value) in enumerate(selected, start=1):
        blocks.append(
            ProtectedBlock(
                id=f"p{idx:03d}",
                kind=kind,
                start_line=line_number_at(text, start),
                end_line=line_number_at(text, end),
                chars=end - start,
                text=value.strip(),
            )
        )
    return blocks


def render(blocks: list[ProtectedBlock], source: str) -> str:
    by_kind: dict[str, int] = {}
    for block in blocks:
        by_kind[block.kind] = by_kind.get(block.kind, 0) + 1

    lines = [
        "# Inventario de bloques protegidos",
        "",
        f"- Fuente: `{source}`",
        f"- Bloques detectados: {len(blocks)}",
    ]
    if by_kind:
        lines.append("- Tipos:")
        for kind, count in sorted(by_kind.items()):
            lines.append(f"  - `{kind}`: {count}")
    lines.extend(
        [
            "",
            "| ID | Tipo | Líneas | Caracteres | Texto compacto |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for block in blocks:
        snippet = compact(block.text).replace("|", "\\|")
        lines.append(f"| {block.id} | {block.kind} | {block.start_line}-{block.end_line} | {block.chars} | {snippet} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Detecta bloques que deben protegerse antes de reescribir.")
    parser.add_argument("input", help="Archivo Markdown/TXT")
    parser.add_argument("--out", help="Ruta Markdown de salida")
    parser.add_argument("--json-out", help="Ruta JSON de salida")
    parser.add_argument('--overwrite', action='store_true', help='Reemplazar informes existentes, nunca entradas')
    args = parser.parse_args()
    try:
        validate_outputs([args.input], [args.out, args.json_out], args.overwrite)
    except ValueError as exc:
        parser.error(str(exc))

    path = Path(args.input)
    text = path.read_text(encoding="utf-8", errors="replace")
    blocks = detect(text)
    report = render(blocks, str(path))

    if args.out:
        atomic_write(args.out, report, overwrite=args.overwrite)
    else:
        sys.stdout.write(report)

    if args.json_out:
        payload = {"source": str(path), "protected_blocks": [asdict(block) for block in blocks]}
        atomic_write(args.json_out, json.dumps(payload, ensure_ascii=False, indent=2), overwrite=args.overwrite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
