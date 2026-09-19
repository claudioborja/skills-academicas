#!/usr/bin/env python3
"""Crear o actualizar un manifiesto JSONL de imágenes editoriales."""

import argparse
import hashlib
import json
from datetime import date
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'workflow-maestro-academico-editorial/scripts'))
from archivos_seguros import atomic_append, atomic_write, validate_outputs


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_record(path: Path) -> dict:
    return {'ruta': str(path.resolve()), 'sha256': sha256(path)}


def ensure_unique_identifier(manifest: Path, identifier: str) -> None:
    if not manifest.exists():
        return
    for line_number, line in enumerate(manifest.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(f"JSON inválido en {manifest}, línea {line_number}") from error
        if isinstance(record, dict) and record.get("id") == identifier:
            raise ValueError(f"El identificador ya existe en el manifiesto: {identifier}")


def restore_file(path: Path, previous: bytes | None) -> None:
    if previous is None:
        path.unlink(missing_ok=True)
    else:
        atomic_write(path, previous, overwrite=True)


def publish_record(manifest: Path, record: str, annex: Path | None = None,
                   annex_entry: str = "") -> None:
    """Publicar el anexo antes del manifiesto y revertirlo si este último falla."""
    if annex is None:
        atomic_append(manifest, record)
        return
    annex_before = annex.read_bytes() if annex.exists() else None
    atomic_append(annex, annex_entry)
    try:
        atomic_append(manifest, record)
    except Exception:
        restore_file(annex, annex_before)
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--id", required=True)
    parser.add_argument("--numero-figura", required=True)
    parser.add_argument("--capitulo", required=True)
    parser.add_argument("--ubicacion", required=True)
    parser.add_argument("--fecha-creacion", required=True,
                        help="Fecha real de creación o adaptación, AAAA-MM-DD")
    parser.add_argument("--estado-revision", default="pendiente_revision_editorial",
                        choices=("pendiente_revision_editorial", "requiere_cambios",
                                 "aprobada", "rechazada"))
    parser.add_argument("--archivo", required=True, type=Path,
                        help="Archivo de trabajo o versión final registrada")
    parser.add_argument("--archivo-original", type=Path,
                        help="Original conservado; por defecto usa --archivo")
    parser.add_argument("--derivado", action="append", default=[], type=Path,
                        help="Archivo derivado; se puede repetir")
    parser.add_argument("--origen", required=True,
                        choices=("descargada", "adaptada", "generada", "elaboracion_propia"))
    parser.add_argument("--metodo", required=True,
                        choices=("manual", "software_convencional", "ia_generativa", "codigo_asistido_ia"))
    parser.add_argument("--funcion", required=True,
                        choices=("evidencia", "reproduccion", "adaptacion", "ilustracion"))
    parser.add_argument("--titulo", required=True)
    parser.add_argument("--fuente", default="")
    parser.add_argument("--url", default="")
    parser.add_argument("--licencia", default="")
    parser.add_argument("--licencia-url", default="")
    parser.add_argument("--necesidad", required=True)
    parser.add_argument("--modelo", default="")
    parser.add_argument("--prompt", default="")
    parser.add_argument("--razon-generacion", default="")
    parser.add_argument("--busqueda-previa", default="")
    parser.add_argument("--anexo", type=Path)
    parser.add_argument("--cambios", default="")
    parser.add_argument("--pie", default="")
    parser.add_argument("--alt", default="")
    args = parser.parse_args()
    original = args.archivo_original or args.archivo
    assets = [args.archivo, original, *args.derivado]
    try:
        validate_outputs(assets, [args.manifest, args.anexo], overwrite=True)
        ensure_unique_identifier(args.manifest, args.id)
        creation_date = date.fromisoformat(args.fecha_creacion)
        if creation_date > date.today():
            raise ValueError("La fecha de creación no puede estar en el futuro")
        for asset in assets:
            if not asset.is_file():
                raise ValueError(f"No existe el archivo de imagen o derivado: {asset}")
        resolved_derivatives = [path.resolve() for path in args.derivado]
        if len(set(resolved_derivatives)) != len(resolved_derivatives):
            raise ValueError("Los archivos derivados no pueden repetirse")
        if any(path in {args.archivo.resolve(), original.resolve()} for path in resolved_derivatives):
            raise ValueError("Un derivado debe ser distinto del original y del archivo de trabajo")
    except (OSError, UnicodeError, ValueError) as exc:
        parser.error(str(exc))

    if args.origen == "descargada":
        if not args.fuente or not args.url or not args.licencia or not args.licencia_url:
            parser.error("Las imágenes descargadas requieren fuente, URL, licencia y URL de licencia open access")
    if args.origen == "generada" and args.funcion != "ilustracion":
        parser.error("Una imagen generada solo puede registrarse como ilustración, no como evidencia documental")
    if args.origen == "adaptada":
        if not all((args.fuente, args.url, args.licencia, args.licencia_url, args.cambios)):
            parser.error("Las adaptaciones requieren fuente, URL, licencia, URL de licencia y cambios realizados")
    assisted = args.metodo in {"ia_generativa", "codigo_asistido_ia"}
    if assisted and args.origen == "elaboracion_propia":
        parser.error("Una imagen asistida por IA no puede registrarse como elaboracion_propia; use generada o adaptada")
    if args.origen in {"generada", "adaptada"} and assisted:
        if not args.modelo or not args.prompt or not args.razon_generacion or not args.busqueda_previa or not args.anexo:
            parser.error("Los recursos asistidos por IA requieren modelo, prompt, razón, búsqueda previa y anexo")
    if args.origen == "generada" and not args.busqueda_previa:
        parser.error("No se puede registrar una generación sin búsqueda previa documentada")

    record = {
        "id": args.id,
        "numero_figura": args.numero_figura,
        "capitulo": args.capitulo,
        "ubicacion_prevista": args.ubicacion,
        "titulo": args.titulo,
        "funcion": args.funcion,
        "origen": args.origen,
        "metodo_creacion": args.metodo,
        "necesidad_editorial": args.necesidad,
        "archivo": str(args.archivo.resolve()),
        "sha256": sha256(args.archivo),
        "archivo_trabajo": file_record(args.archivo),
        "archivo_original": file_record(original),
        "derivados": [file_record(path) for path in args.derivado],
        "fuente": args.fuente,
        "url": args.url,
        "licencia": args.licencia,
        "licencia_url": args.licencia_url,
        "fecha_creacion": args.fecha_creacion,
        "fecha_registro": date.today().isoformat(),
        "fecha_consulta": date.today().isoformat(),
        "cambios": args.cambios,
        "modelo": args.modelo,
        "busqueda_previa": args.busqueda_previa,
        "razon_generacion": args.razon_generacion,
        "anexo_prompt": str(args.anexo.resolve()) if args.anexo else "",
        "pie": args.pie,
        "texto_alternativo": args.alt,
        "estado": args.estado_revision,
        "estado_revision": args.estado_revision,
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    annex_entry = ""
    if assisted:
        args.anexo.parent.mkdir(parents=True, exist_ok=True)
        heading = "# Anexo de prompts y razones de recursos generados\n\n" if not args.anexo.exists() else ""
        annex_entry = heading + (
                f"## Imagen {args.id}: {args.titulo}\n\n"
                f"- **Origen:** {args.origen}\n"
                f"- **Método:** {args.metodo}\n"
                f"- **Modelo:** {args.modelo}\n"
                f"- **Fecha de generación o adaptación:** {args.fecha_creacion}\n"
                f"- **Necesidad editorial:** {args.necesidad}\n"
                f"- **Razón de generación o adaptación:** {args.razon_generacion}\n"
                f"- **Búsqueda previa:** {args.busqueda_previa}\n\n"
                f"### Prompt literal\n\n```text\n{args.prompt}\n```\n\n"
        )
    publish_record(args.manifest, json.dumps(record, ensure_ascii=False) + "\n",
                   args.anexo if assisted else None, annex_entry)
    print(f"Registro añadido a {args.manifest}")


if __name__ == "__main__":
    main()
