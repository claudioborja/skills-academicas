#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'editor-en-jefe/scripts'))
from archivos_seguros import atomic_write, validate_outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("audit", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument('--overwrite', action='store_true', help='Reemplazar informes existentes, nunca entradas')
    args = parser.parse_args()
    try:
        validate_outputs([args.audit], [args.out], args.overwrite)
    except ValueError as exc:
        parser.error(str(exc))

    text = args.audit.read_text(encoding="utf-8")
    entries = re.split(r"\n-{20,}\n", text)
    lines = [
        "Resumen de citas con respaldo debil",
        "",
        "Estas entradas requieren revision manual del PDF, ajuste del parrafo del libro o sustitucion de la cita.",
        "",
    ]
    count = 0
    for entry in entries:
        if "Alerta: respaldo debil" not in entry:
            continue
        count += entry.count("Alerta: respaldo debil")
        location = re.search(r"Ubicacion en el libro: (.+)", entry)
        paragraph = re.search(r"Parrafo del libro: (.+)", entry)
        refs = re.findall(
            r"Referencia \[(\d+)\]: (.+?)\nArchivo PDF: (.+?)\nParrafo fuente: (.+?)\n(?:Puntaje de afinidad textual: ([0-9.]+)\n)?Que dice el documento fuente: (.+?)\nPor que respalda la cita: (.+?)(?=\n(?:Alerta|Referencia|\Z))",
            entry,
            flags=re.S,
        )
        weak_refs = [ref for ref in refs if "Alerta: respaldo debil" in entry[entry.find(f"Referencia [{ref[0]}]"):]]
        lines.append(f"Ubicacion: {location.group(1) if location else 'No identificada'}")
        if paragraph:
            lines.append(f"Parrafo del libro: {paragraph.group(1)[:550].strip()}...")
        for rid, label, pdf, source, score, source_text, why in weak_refs:
            lines.append(f"- Referencia [{rid}] {label.strip()}")
            lines.append(f"  PDF: {pdf.strip()}")
            lines.append(f"  Fuente localizada: {source.strip()}")
            if score:
                lines.append(f"  Puntaje: {score}")
            lines.append(f"  Fragmento fuente: {re.sub(r'\\s+', ' ', source_text).strip()[:360]}...")
            lines.append(f"  Motivo de alerta: {why.strip()}")
        lines.append("")
    lines.insert(3, f"Total de alertas: {count}")
    lines.insert(4, "")
    atomic_write(args.out, "\n".join(lines), overwrite=args.overwrite)
    print(f"Resumen creado: {args.out}")
    print(f"Alertas: {count}")


if __name__ == "__main__":
    main()
