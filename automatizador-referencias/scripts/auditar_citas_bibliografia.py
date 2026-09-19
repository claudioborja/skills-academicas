#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'workflow-maestro-academico-editorial/scripts'))
from archivos_seguros import atomic_write, validate_outputs


NUM_CITE_RE = re.compile(
    r"\[(?P<numbers>\d+(?:\s*[-–,]\s*\d+)*)(?:,\s*(?:pp?\.|Ch\.|Sec\.|Fig\.|eq\.|Th\.|Lemma|Appendix|Algorithm)\s*[^\]\n]+)?\]"
    r"(?:\s*[-–]\s*\[(?P<end>\d+)\])?", re.I)
NUM_REF_RE = re.compile(r"(?m)^\s*\[(\d+)\]\s+(.+)$")
APA_CITE_RE = re.compile(r"\(([A-ZÁÉÍÓÚÑ][A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+),\s*((?:19|20)\d{2}[a-z]?)")
DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.I)
REF_HEADING_RE = re.compile(r"(?im)^[ \t]*(?:#{1,6}[ \t]+)?(?:referencias|bibliograf[ií]a|references)[ \t]*$")


@dataclass
class Audit:
    numeric_citations: list[int]
    numeric_references: list[int]
    missing_numeric_references: list[int]
    uncited_numeric_references: list[int]
    apa_citations: list[str]
    doi_count: int
    doi_values: list[str]
    style_signals: list[str]
    warnings: list[str]
    first_appearance: list[int] = field(default_factory=list)
    duplicate_reference_numbers: list[int] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def expand_numeric(value: str) -> list[int]:
    nums: list[int] = []
    for part in re.split(r"\s*,\s*", value):
        if re.search(r"[-–]", part):
            a, b = [int(x.strip()) for x in re.split(r"[-–]", part, maxsplit=1)]
            if b < a or b - a > 10000:
                raise ValueError("Rango descendente o demasiado grande; revisar manualmente.")
            nums.extend(range(a, b + 1))
        else:
            nums.append(int(part.strip()))
    return nums


def split_body_refs(text: str) -> tuple[str, str]:
    match = REF_HEADING_RE.search(text)
    if not match:
        return text, ""
    tail = text[match.end():]
    end = re.search(r"(?m)^#{1,6}\s+|^(?:Apéndice|Appendix|Anexo)\b", tail)
    if end:
        return text[:match.start()] + "\n" + tail[end.start():], tail[:end.start()]
    return text[:match.start()], tail


def audit(text: str, style: str = "auto") -> Audit:
    text = re.sub(r"(?ms)^\s*(`{3,}|~{3,})[^\n]*\n.*?^\s*\1[^\n]*$", "", text)
    text = re.sub(r"`[^`\n]*`", "", text)
    body, refs = split_body_refs(text)
    errors = []
    warnings = ["Control mecánico parcial: verificar atribución, metadatos y formato final manualmente."]
    ordered = []
    for match in NUM_CITE_RE.finditer(body):
        numbers = match.group('numbers')
        if match.group('end'):
            numbers += '-' + match.group('end')
        if re.search(r'[-–]', numbers):
            warnings.append("Rango de citas: escribir cada número por separado en el perfil IEEE actual.")
            if style == 'ieee':
                errors.append("Rango comprimido de citas en perfil IEEE.")
        elif ',' in numbers and style == 'ieee':
            errors.append("Separar citas múltiples en corchetes individuales.")
        try:
            ordered.extend(expand_numeric(numbers))
        except ValueError as exc:
            errors.append(str(exc))
    first = list(dict.fromkeys(ordered))
    numeric_citations = sorted(set(ordered))
    ref_order = [int(m.group(1)) for m in NUM_REF_RE.finditer(refs)]
    numeric_references = sorted(set(ref_order))
    duplicates = sorted(n for n, count in Counter(ref_order).items() if count > 1)
    if duplicates:
        errors.append(f"Números de referencia duplicados: {duplicates}.")
    if first and first != list(range(1, len(first) + 1)):
        warnings.append(f"Revisar orden de primera aparición: {first}; si es un fragmento, contrastar con la obra completa.")
        if style == 'ieee':
            errors.append("Orden de primera aparición no consecutivo desde 1.")
    if ref_order and ref_order != list(range(1, len(ref_order) + 1)):
        warnings.append("Orden o numeración de la lista de referencias no consecutivo desde 1.")
        if style == 'ieee':
            errors.append("Orden o numeración incorrectos en lista de referencias.")
    if not REF_HEADING_RE.search(text):
        warnings.append("No se identificó sección de referencias; no se infiere bibliografía a partir de citas.")
    missing = sorted(set(numeric_citations) - set(numeric_references))
    if missing:
        errors.append(f"Citas numéricas sin referencia: {missing}.")
    warnings.extend(errors)
    apa_citations = sorted({f"{m.group(1)}, {m.group(2)}" for m in APA_CITE_RE.finditer(body)})
    dois = sorted({m.group(0).rstrip(".,;)").lower() for m in DOI_RE.finditer(text)})
    style_signals = []
    if numeric_citations or numeric_references:
        style_signals.append("ieee_numeric")
    if apa_citations:
        style_signals.append("apa_author_year")
    if "ieee_numeric" in style_signals and "apa_author_year" in style_signals:
        warnings.append("Mezcla probable de citación IEEE numérica y APA autor-año.")
    if numeric_citations and not numeric_references:
        warnings.append("Hay citas numéricas, pero no se detectó bibliografía numerada.")
    if numeric_references and not numeric_citations:
        warnings.append("Hay referencias numeradas, pero no se detectaron citas numéricas en el cuerpo.")
    return Audit(
        numeric_citations=numeric_citations,
        numeric_references=numeric_references,
        missing_numeric_references=sorted(set(numeric_citations) - set(numeric_references)),
        uncited_numeric_references=sorted(set(numeric_references) - set(numeric_citations)),
        apa_citations=apa_citations,
        doi_count=len(dois),
        doi_values=dois,
        style_signals=style_signals,
        warnings=warnings,
        first_appearance=first,
        duplicate_reference_numbers=duplicates,
        errors=errors,
    )


def render(result: Audit, source: str) -> str:
    lines = [
        "# Auditoría de citas y bibliografía",
        "",
        f"- Fuente: `{source}`",
        f"- Señales de estilo: {', '.join(result.style_signals) if result.style_signals else 'No detectadas'}",
        f"- Citas numéricas: {len(result.numeric_citations)}",
        f"- Referencias numeradas: {len(result.numeric_references)}",
        f"- Citas APA probables: {len(result.apa_citations)}",
        f"- DOI detectados: {result.doi_count}",
    ]
    if result.warnings:
        lines.append("- Advertencias:")
        lines.extend(f"  - {w}" for w in result.warnings)
    lines.extend(["", "## Faltantes", ""])
    lines.append("- Citas numéricas sin referencia: " + (", ".join(map(str, result.missing_numeric_references)) or "Ninguna"))
    lines.append("- Referencias numeradas no citadas: " + (", ".join(map(str, result.uncited_numeric_references)) or "Ninguna"))
    if result.doi_values:
        lines.extend(["", "## DOI", ""])
        lines.extend(f"- `{doi}`" for doi in result.doi_values)
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Audita citas en cuerpo y bibliografía final.")
    parser.add_argument("input")
    parser.add_argument("--out")
    parser.add_argument("--json-out")
    parser.add_argument("--style", choices=("auto", "ieee", "apa"), default="auto")
    parser.add_argument("--strict", action="store_true", help="Salir con código 1 si hay errores mecánicos; no certifica la norma")
    parser.add_argument('--overwrite', action='store_true', help='Autorizar reemplazo de informes, nunca de entradas')
    args = parser.parse_args()
    try:
        validate_outputs([args.input], [args.out, args.json_out], args.overwrite)
    except ValueError as exc:
        parser.error(str(exc))
    path = Path(args.input)
    result = audit(path.read_text(encoding="utf-8", errors="replace"), args.style)
    report = render(result, str(path))
    if args.out:
        atomic_write(args.out, report, overwrite=args.overwrite)
    else:
        sys.stdout.write(report)
    if args.json_out:
        atomic_write(args.json_out, json.dumps(asdict(result), ensure_ascii=False, indent=2), overwrite=args.overwrite)
    return 1 if args.strict and result.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
