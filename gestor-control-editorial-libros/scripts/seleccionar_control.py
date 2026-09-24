#!/usr/bin/env python3
"""Selecciona el perfil de control editorial de un libro desde contexto JSON."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
import tempfile


TIPOS_OBRA = {
    "tesis-convertida",
    "monografia",
    "obra-colectiva",
    "volumen-editado",
    "otro",
}
AUTORIAS = {"integral", "independiente", "por-determinar"}
ETAPAS = {"recepcion", "pre-revision", "aceptada", "prepublicacion"}

ASSETS = {
    "ficha_control": "assets/01_Ficha_control_editorial_libros_EUC.docx",
    "instructivo_control": "assets/02_Instructivo_ficha_control_editorial_EUC.docx",
    "perfil_bkci": "assets/03_Guia_18_criterios_BKCI_EUC.docx",
    "obra-completa": "assets/04_Plantilla_front_matter_obra_completa_EUC.docx",
    "libro-por-capitulos": "assets/05_Plantilla_front_matter_libro_por_capitulos_EUC.docx",
    "instructivo_front_matter": "assets/06_Instructivo_front_matter_EUC.docx",
}


def validate_context(data: object) -> dict:
    if not isinstance(data, dict):
        raise ValueError("El contexto debe ser un objeto JSON")
    if data.get("tipo_obra") not in TIPOS_OBRA:
        raise ValueError(f"tipo_obra no admitido: {data.get('tipo_obra')!r}")
    if data.get("autoria_capitulos") not in AUTORIAS:
        raise ValueError(
            f"autoria_capitulos no admitida: {data.get('autoria_capitulos')!r}"
        )
    if data.get("etapa") not in ETAPAS:
        raise ValueError(f"etapa no admitida: {data.get('etapa')!r}")
    if not isinstance(data.get("objetivo_bkci"), bool):
        raise ValueError("objetivo_bkci debe ser booleano")
    return data


def select_control(data: dict) -> dict:
    authorship = data["autoria_capitulos"]
    stage = data["etapa"]
    profile = {
        "integral": "obra-completa",
        "independiente": "libro-por-capitulos",
        "por-determinar": None,
    }[authorship]

    controls = [
        "control-admisibilidad"
        if stage in {"recepcion", "pre-revision"}
        else "control-tecnico-prepublicacion"
    ]
    if data["objetivo_bkci"]:
        controls.append("preevaluacion-bkci")

    decisions = []
    if profile is None:
        decisions.append(
            "Confirmar si la autoría pertenece a la obra integral o a capítulos independientes."
        )

    resources = {
        "ficha_control": ASSETS["ficha_control"],
        "instructivo_control": ASSETS["instructivo_control"],
        "instructivo_front_matter": ASSETS["instructivo_front_matter"],
        "plantilla": ASSETS[profile] if profile else None,
        "perfil_bkci": ASSETS["perfil_bkci"] if data["objetivo_bkci"] else None,
    }

    warnings = [
        "La selección orienta el control editorial, pero no decide la aceptación científica.",
        "No corregir datos de autoría, afiliación, ORCID, ISBN, DOI, licencia o ética sin evidencia y confirmación.",
    ]
    if data["objetivo_bkci"]:
        warnings.extend(
            [
                "La preevaluación BKCI no garantiza selección ni cobertura por Clarivate.",
                "Antes de aplicarla, comprobar los criterios vigentes en la fuente oficial de Clarivate.",
            ]
        )

    return {
        "tipo_obra": data["tipo_obra"],
        "etapa": stage,
        "perfil_front_matter": profile,
        "controles": controls,
        "estado": "REQUIERE_DECISION_EDITORIAL" if decisions else "PERFIL_RECOMENDADO",
        "decisiones_pendientes": decisions,
        "recursos": resources,
        "advertencias": warnings,
    }


def atomic_write(path: Path, content: str, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"La salida ya existe: {path}")
    if path.is_symlink():
        raise ValueError(f"No se escribe sobre enlaces simbólicos: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
        ) as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
            temporary = Path(handle.name)
        if overwrite:
            os.replace(temporary, path)
        else:
            os.link(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Contexto JSON del libro")
    parser.add_argument("--out", type=Path, help="Informe JSON opcional")
    parser.add_argument(
        "--permitir-sobrescritura",
        action="store_true",
        help="Permitir reemplazar el informe, nunca la entrada",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        source = args.input.resolve(strict=True)
        if not source.is_file():
            raise ValueError(f"La entrada no es un archivo: {source}")
        data = validate_context(json.loads(source.read_text(encoding="utf-8")))
        report = json.dumps(select_control(data), ensure_ascii=False, indent=2) + "\n"
        if args.out is None:
            print(report, end="")
            return 0
        output = args.out.resolve()
        if output == source:
            raise ValueError("La salida no puede reemplazar la entrada")
        atomic_write(output, report, args.permitir_sobrescritura)
        print(json.dumps({"status": "ok", "out": str(output)}, ensure_ascii=False))
        return 0
    except (FileExistsError, json.JSONDecodeError, OSError, UnicodeError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
