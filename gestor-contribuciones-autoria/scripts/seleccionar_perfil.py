#!/usr/bin/env python3
"""Recomienda un perfil de contribución, autoría y metadatos desde contexto JSON."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
import tempfile


TIPOS_OBRA = {
    "articulo",
    "revision",
    "tesis",
    "informe",
    "dataset",
    "software",
    "libro",
    "capitulo",
    "traduccion",
    "catalogo",
    "otro",
}
DISCIPLINAS = {
    "general",
    "biomedicina",
    "ingenieria",
    "humanidades",
    "ciencias-sociales",
    "otra",
}
DESTINOS = {
    "jats": "JATS XML",
    "crossref": "Crossref",
    "datacite": "DataCite",
    "orcid": "ORCID",
    "codemeta": "CodeMeta",
    "cff": "Citation File Format",
    "marc": "MARC 21",
    "grafo": "PROV-O",
}
PRODUCTOS_BIBLIOGRAFICOS = {"libro", "capitulo", "traduccion", "catalogo"}


def unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def require_boolean(data: dict, key: str) -> bool:
    value = data.get(key)
    if not isinstance(value, bool):
        raise ValueError(f"{key} debe ser booleano")
    return value


def validate_context(data: object) -> dict:
    if not isinstance(data, dict):
        raise ValueError("El contexto debe ser un objeto JSON")
    tipo = data.get("tipo_obra")
    if tipo not in TIPOS_OBRA:
        raise ValueError(f"tipo_obra no admitido: {tipo!r}")
    disciplina = data.get("disciplina")
    if disciplina not in DISCIPLINAS:
        raise ValueError(f"disciplina no admitida: {disciplina!r}")
    require_boolean(data, "salida_investigacion")
    require_boolean(data, "decidir_autoria")
    destinos = data.get("destinos")
    if not isinstance(destinos, list) or any(not isinstance(item, str) for item in destinos):
        raise ValueError("destinos debe ser una lista de cadenas")
    desconocidos = [item for item in destinos if item not in DESTINOS]
    if desconocidos:
        raise ValueError(f"destinos no admitidos: {', '.join(desconocidos)}")
    return data


def select_profile(data: dict) -> dict:
    tipo = data["tipo_obra"]
    disciplina = data["disciplina"]
    research = data["salida_investigacion"]
    decide_authorship = data["decidir_autoria"]
    destinations = data["destinos"]

    taxonomies: list[str] = []
    if research:
        primary = "CRediT"
        taxonomies.append("CRediT")
    elif tipo in PRODUCTOS_BIBLIOGRAFICOS:
        primary = "MARC Relator Terms"
        taxonomies.append("MARC Relator Terms")
    else:
        primary = "Política específica del producto"

    if tipo == "dataset" or "datacite" in destinations:
        taxonomies.append("DataCite Contributor Types")
    if (tipo in PRODUCTOS_BIBLIOGRAFICOS or "marc" in destinations) and "MARC Relator Terms" not in taxonomies:
        taxonomies.append("MARC Relator Terms")
    if "grafo" in destinations:
        taxonomies.append("CRO")

    representation: list[str] = []
    if tipo == "dataset":
        representation.append("DataCite")
    if tipo == "software":
        representation.extend(["CodeMeta", "Citation File Format"])
    if tipo in PRODUCTOS_BIBLIOGRAFICOS:
        representation.append("MARC 21")
    representation.extend(DESTINOS[item] for item in destinations)

    authorship: list[str] = []
    integrity: list[str] = []
    requires_policy = False
    if decide_authorship:
        integrity.append("COPE")
        if disciplina == "biomedicina":
            authorship.append("ICMJE")
        else:
            authorship.append("Política de la revista, editorial o institución")
            requires_policy = True

    warnings = [
        "CRediT describe contribuciones, pero no decide autoría ni el orden de firma.",
        "La recomendación no asigna roles a personas sin evidencia y confirmación de los participantes.",
    ]
    if decide_authorship:
        warnings.append("Aplicar primero la política vigente del destino editorial y documentar cualquier conflicto.")

    return {
        "perfil_principal": primary,
        "taxonomias": unique(taxonomies),
        "criterios_autoria": authorship,
        "integridad_y_disputas": integrity,
        "representacion": unique(representation),
        "identificadores": ["ORCID iD autenticado"] if "orcid" in destinations else [],
        "requiere_politica_autoria": requires_policy,
        "estado": "REQUIERE_POLITICA_AUTORIA" if requires_policy else "PERFIL_RECOMENDADO",
        "advertencias": warnings,
    }


def atomic_write(path: Path, content: str) -> None:
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
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Contexto JSON de la obra")
    parser.add_argument("--out", type=Path, help="Informe JSON opcional")
    parser.add_argument(
        "--permitir-sobrescritura",
        action="store_true",
        help="Permitir reemplazar el informe de salida, nunca la entrada",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        source = args.input.resolve(strict=True)
        if not source.is_file():
            raise ValueError(f"La entrada no es un archivo: {source}")
        data = validate_context(json.loads(source.read_text(encoding="utf-8")))
        report = json.dumps(select_profile(data), ensure_ascii=False, indent=2) + "\n"
        if args.out is None:
            print(report, end="")
            return 0
        output = args.out.resolve()
        if output == source:
            raise ValueError("La salida no puede reemplazar la entrada")
        if output.exists() and not args.permitir_sobrescritura:
            raise FileExistsError(f"La salida ya existe: {output}")
        atomic_write(output, report)
        print(json.dumps({"status": "ok", "out": str(output)}, ensure_ascii=False))
        return 0
    except (FileExistsError, json.JSONDecodeError, OSError, UnicodeError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
