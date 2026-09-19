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


TYPE_PATTERNS = {
    "cita_referencia": re.compile(r"(?i)\b(cita|referencia|bibliograf|doi|fuente)\b"),
    "metodo": re.compile(r"(?i)\b(m[eé]todo|metodolog|muestra|instrumento|an[aá]lisis)\b"),
    "estructura": re.compile(r"(?i)\b(estructura|orden|secci[oó]n|cap[ií]tulo|apartado)\b"),
    "redaccion": re.compile(r"(?i)\b(redacci[oó]n|claridad|estilo|ortograf|coherencia)\b"),
    "resultado": re.compile(r"(?i)\b(resultado|hallazgo|discusi[oó]n|conclusi[oó]n)\b"),
}


@dataclass
class Observation:
    id: str
    comment: str
    type: str
    severity: str
    action: str
    status: str


def split_comments(text: str) -> list[str]:
    lines = [line.strip() for line in text.splitlines()]
    comments: list[str] = []
    buffer = ""
    marker = re.compile(r"^(?:[-*]|\d+[.)]|observaci[oó]n\s+\d+[:.)-])\s*(.+)$", re.I)
    for line in lines:
        if not line:
            if buffer:
                comments.append(buffer.strip())
                buffer = ""
            continue
        match = marker.match(line)
        if match:
            if buffer:
                comments.append(buffer.strip())
            buffer = match.group(1)
        elif buffer:
            buffer += " " + line
        else:
            buffer = line
    if buffer:
        comments.append(buffer.strip())
    return [c for c in comments if c]


def classify(comment: str) -> tuple[str, str, str]:
    found = [name for name, pattern in TYPE_PATTERNS.items() if pattern.search(comment)]
    ctype = found[0] if found else "general"
    severity = "alta" if re.search(r"(?i)\b(no cumple|falta|debe|obligatorio|inconsistente)\b", comment) else "media"
    action = {
        "cita_referencia": "Verificar fuente, cita y bibliografía",
        "metodo": "Aclarar diseño, muestra, procedimiento o análisis",
        "estructura": "Reordenar o completar sección",
        "redaccion": "Reescribir con mayor claridad y coherencia",
        "resultado": "Alinear resultado, discusión y conclusión",
        "general": "Revisar y decidir cambio",
    }[ctype]
    return ctype, severity, action


def build(text: str) -> list[Observation]:
    result: list[Observation] = []
    for idx, comment in enumerate(split_comments(text), start=1):
        ctype, severity, action = classify(comment)
        result.append(Observation(f"obs-{idx:03d}", comment, ctype, severity, action, "pendiente"))
    return result


def render(items: list[Observation], source: str) -> str:
    lines = ["# Matriz de observaciones", "", f"- Fuente: `{source}`", f"- Observaciones: {len(items)}", "", "| ID | Tipo | Severidad | Estado | Acción sugerida | Comentario |", "| --- | --- | --- | --- | --- | --- |"]
    for item in items:
        comment = item.comment.replace("|", "\\|")
        lines.append(f"| {item.id} | {item.type} | {item.severity} | {item.status} | {item.action} | {comment} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Convierte observaciones dispersas en matriz de respuesta.")
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
    items = build(path.read_text(encoding="utf-8", errors="replace"))
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
