#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'workflow-maestro-academico-editorial/scripts'))
from archivos_seguros import atomic_write, validate_outputs


WORD_RE = re.compile(r"\b\w+\b", re.UNICODE)
HEAD_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.M)
SECTIONS = {
    "resumen": re.compile(r"(?i)\b(resumen|abstract)\b"),
    "introduccion": re.compile(r"(?i)\b(introducci[oó]n|introduction)\b"),
    "metodos": re.compile(r"(?i)\b(m[eé]todos?|metodolog[ií]a|materials? and methods?)\b"),
    "resultados": re.compile(r"(?i)\b(resultados|results?|hallazgos|findings)\b"),
    "discusion": re.compile(r"(?i)\b(discusi[oó]n|discussion)\b"),
    "conclusiones": re.compile(r"(?i)\b(conclusiones?|conclusions?)\b"),
    "referencias": re.compile(r"(?i)\b(referencias|bibliograf[ií]a|references)\b"),
}
SIGNALS = {
    "objetivo": re.compile(r"(?i)\b(objetivo|prop[oó]sito|aim|objective)\b"),
    "muestra": re.compile(r"(?i)\b(muestra|participantes|corpus|sample|dataset|poblaci[oó]n)\b"),
    "analisis": re.compile(r"(?i)\b(an[aá]lisis|estad[ií]stic|software|codificaci[oó]n|analysis)\b"),
    "limitaciones": re.compile(r"(?i)\b(limitaci[oó]n|limitaciones|limitations?)\b"),
}


def split_sections(text: str) -> dict[str, str]:
    matches = list(HEAD_RE.finditer(text))
    chunks: dict[str, str] = {}
    for idx, match in enumerate(matches):
        title = match.group(2).strip()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        body = text[match.start():end]
        for key, pattern in SECTIONS.items():
            if pattern.search(title):
                chunks[key] = body
                break
    return chunks


def audit(text: str) -> dict:
    chunks = split_sections(text)
    present = {key: key in chunks for key in SECTIONS}
    section_words = {key: len(WORD_RE.findall(value)) for key, value in chunks.items()}
    warnings = []
    for key in ("introduccion", "metodos", "resultados", "discusion"):
        if not present.get(key):
            warnings.append({"severity": "alta", "message": f"Falta sección IMRyD: {key}."})
    if present.get("introduccion") and not SIGNALS["objetivo"].search(chunks["introduccion"]):
        warnings.append({"severity": "media", "message": "La introducción no contiene señal clara de objetivo."})
    if present.get("metodos") and not SIGNALS["muestra"].search(chunks["metodos"]):
        warnings.append({"severity": "media", "message": "Métodos no menciona muestra, corpus o participantes."})
    if present.get("metodos") and not SIGNALS["analisis"].search(chunks["metodos"]):
        warnings.append({"severity": "media", "message": "Métodos no menciona técnica de análisis."})
    if present.get("discusion") and not SIGNALS["limitaciones"].search(chunks["discusion"]):
        warnings.append({"severity": "baja", "message": "Discusión no menciona limitaciones."})
    return {"present": present, "section_words": section_words, "warnings": warnings}


def render(payload: dict, source: str) -> str:
    lines = ["# Auditoría IMRyD", "", f"- Fuente: `{source}`", "", "| Sección | Presente | Palabras |", "| --- | --- | --- |"]
    for key in SECTIONS:
        lines.append(f"| {key} | {str(payload['present'].get(key, False)).lower()} | {payload['section_words'].get(key, 0)} |")
    if payload["warnings"]:
        lines.extend(["", "## Advertencias", ""])
        lines.extend(f"- `{w['severity']}`: {w['message']}" for w in payload["warnings"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Audita estructura IMRyD/IMRAD.")
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
