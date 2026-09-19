#!/usr/bin/env python3
"""Registrar procedencia y necesidad de una tabla editorial."""

import argparse
import json
from datetime import date
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'workflow-maestro-academico-editorial/scripts'))
from archivos_seguros import atomic_append, validate_outputs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--id", required=True)
    parser.add_argument("--titulo", required=True)
    parser.add_argument("--origen", required=True,
                        choices=("copiada", "traducida", "adaptada", "generada", "elaboracion_propia"))
    parser.add_argument("--necesidad", required=True)
    parser.add_argument("--fuente", default="")
    parser.add_argument("--url", default="")
    parser.add_argument("--licencia", default="")
    parser.add_argument("--licencia-url", default="")
    parser.add_argument("--cambios", default="")
    parser.add_argument("--modelo", default="")
    parser.add_argument("--prompt", default="")
    parser.add_argument("--razon-generacion", default="")
    parser.add_argument("--anexo", type=Path)
    args = parser.parse_args()
    try:
        validate_outputs([], [args.manifest, args.anexo], overwrite=True)
    except ValueError as exc:
        parser.error(str(exc))

    if args.origen in {"copiada", "traducida", "adaptada"}:
        if not all((args.fuente, args.url, args.licencia, args.licencia_url)):
            parser.error("Una tabla externa requiere fuente, URL, licencia y URL de licencia open access")
    if args.origen == "traducida" and not args.cambios:
        parser.error("Una tabla traducida debe describir la traducción en --cambios")
    if args.origen == "generada" and not all((args.modelo, args.prompt, args.razon_generacion, args.anexo)):
        parser.error("Una tabla generada requiere modelo, prompt, razón y anexo separado")

    record = {
        "id": args.id, "titulo": args.titulo, "origen": args.origen,
        "necesidad_editorial": args.necesidad, "fuente": args.fuente,
        "url": args.url, "licencia": args.licencia,
        "licencia_url": args.licencia_url, "cambios": args.cambios,
        "modelo": args.modelo, "fecha_registro": date.today().isoformat(),
        "estado": "pendiente_revision_editorial",
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    atomic_append(args.manifest, json.dumps(record, ensure_ascii=False) + "\n")

    if args.origen == "generada":
        args.anexo.parent.mkdir(parents=True, exist_ok=True)
        heading = "# Anexo de prompts y razones de recursos generados\n\n" if not args.anexo.exists() else ""
        atomic_append(args.anexo, heading + (
                f"## Tabla {args.id}: {args.titulo}\n\n"
                f"- **Modelo:** {args.modelo}\n"
                f"- **Fecha de generación:** {date.today().isoformat()}\n"
                f"- **Necesidad editorial:** {args.necesidad}\n"
                f"- **Razón de generación:** {args.razon_generacion}\n\n"
                f"### Prompt literal\n\n```text\n{args.prompt}\n```\n\n"
        ))
    print(f"Registro añadido a {args.manifest}")


if __name__ == "__main__":
    main()
