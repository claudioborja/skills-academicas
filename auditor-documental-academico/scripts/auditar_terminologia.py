#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'workflow-maestro-academico-editorial/scripts'))
from archivos_seguros import atomic_write, validate_outputs


ACRONYM_RE = re.compile(r"\b[A-ZÁÉÍÓÚÑ]{2,}\b")


@dataclass
class Term:
    term: str
    normalized: str
    count: int
    variants: list[str]


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", value.lower()).strip()


def audit(text: str, terms: list[str]) -> list[Term]:
    candidates = set(terms)
    candidates.update(ACRONYM_RE.findall(text))
    result: list[Term] = []
    for term in sorted(candidates, key=str.lower):
        if not term:
            continue
        pattern = re.compile(rf"\b{re.escape(term)}\b", re.I)
        matches = pattern.findall(text)
        if matches:
            result.append(Term(term=term, normalized=normalize(term), count=len(matches), variants=sorted(set(matches))))
    return result


def render(items: list[Term], source: str) -> str:
    lines = ["# Auditoría terminológica", "", f"- Fuente: `{source}`", f"- Términos detectados: {len(items)}", "", "| Término | Normalizado | Frecuencia | Variantes |", "| --- | --- | --- | --- |"]
    for item in items:
        lines.append(f"| {item.term.replace('|', '\\|')} | {item.normalized} | {item.count} | {', '.join(item.variants).replace('|', '\\|')} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Cuenta términos, siglas y variantes visibles.")
    parser.add_argument("input")
    parser.add_argument("--terms", nargs="*", default=[])
    parser.add_argument("--out")
    parser.add_argument("--json-out")
    parser.add_argument('--overwrite', action='store_true', help='Autorizar reemplazo de informes, nunca de entradas')
    args = parser.parse_args()
    try:
        validate_outputs([args.input], [args.out, args.json_out], args.overwrite)
    except ValueError as exc:
        parser.error(str(exc))
    path = Path(args.input)
    items = audit(path.read_text(encoding="utf-8", errors="replace"), args.terms)
    report = render(items, str(path))
    if args.out:
        atomic_write(args.out, report, overwrite=args.overwrite)
    else:
        sys.stdout.write(report)
    if args.json_out:
        atomic_write(args.json_out, json.dumps([asdict(i) for i in items], ensure_ascii=False, indent=2), overwrite=args.overwrite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
