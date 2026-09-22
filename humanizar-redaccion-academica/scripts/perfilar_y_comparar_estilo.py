#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import tempfile
from pathlib import Path

import comparar_con_perfil_estilo as comparator
import documento_a_perfil_estilo as profiler

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'editor-en-jefe/scripts'))
from archivos_seguros import atomic_write, validate_outputs


def write(path: Path, text: str, overwrite=False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    atomic_write(path, text, overwrite)


def write_json(path: Path, payload: object, overwrite=False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    atomic_write(path, json.dumps(payload, ensure_ascii=False, indent=2), overwrite)


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    value = re.sub(r"[\s_]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "estilo"


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def write_canonical_outputs(out_dir: Path, profile: dict, result: dict, style_name: str, model_paths: list[Path], draft_path: Path, overwrite=False) -> dict[str, Path]:
    paths = {
        "profile_md": out_dir / "perfil.md",
        "profile_json": out_dir / "perfil.json",
        "diagnosis_md": out_dir / "diagnostico.md",
        "diagnosis_json": out_dir / "diagnostico.json",
        "summary_md": out_dir / "resumen.md",
        "manifest_json": out_dir / "manifest.json",
    }
    validate_outputs([*model_paths, draft_path], list(paths.values()), overwrite)
    write(paths["profile_md"], profiler.render(profile), overwrite)
    write_json(paths["profile_json"], profile, overwrite)
    write(paths["diagnosis_md"], comparator.render(result), overwrite)
    write_json(paths["diagnosis_json"], result, overwrite)
    manifest = {
        "style_name": style_name,
        "style_slug": out_dir.name,
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "model_files": [str(path) for path in model_paths],
        "draft_file": str(draft_path),
        "files": {key: str(path) for key, path in paths.items() if key != "manifest_json"},
    }
    write_json(paths["manifest_json"], manifest, overwrite)
    summary = [
        "# Perfil y comparacion de estilo",
        "",
        f"- Estilo: `{style_name}`",
        f"- Carpeta canonica: `{out_dir}`",
        f"- Perfil Markdown: `{paths['profile_md']}`",
        f"- Perfil JSON: `{paths['profile_json']}`",
        f"- Diagnostico Markdown: `{paths['diagnosis_md']}`",
        f"- Diagnostico JSON: `{paths['diagnosis_json']}`",
        f"- Manifest: `{paths['manifest_json']}`",
        "",
        "## Siguiente paso",
        "",
        "Usar el diagnostico como brief de reescritura. No copiar frases del modelo ni modificar contenido protegido.",
        "",
    ]
    write(paths["summary_md"], "\n".join(summary), overwrite)
    return paths


def write_legacy_copy(out_dir: Path, prefix: str, profile: dict, result: dict, overwrite=False) -> Path:
    profile_md = out_dir / f"{prefix}_perfil.md"
    profile_json = out_dir / f"{prefix}_perfil.json"
    diagnosis_md = out_dir / f"{prefix}_diagnostico.md"
    diagnosis_json = out_dir / f"{prefix}_diagnostico.json"
    summary_md = out_dir / f"{prefix}_resumen.md"
    validate_outputs([], [profile_md, profile_json, diagnosis_md, diagnosis_json, summary_md], overwrite)
    write(profile_md, profiler.render(profile), overwrite)
    write_json(profile_json, profile, overwrite)
    write(diagnosis_md, comparator.render(result), overwrite)
    write_json(diagnosis_json, result, overwrite)
    summary = [
        "# Copia de perfil y comparacion de estilo",
        "",
        f"- Perfil Markdown: `{profile_md}`",
        f"- Perfil JSON: `{profile_json}`",
        f"- Diagnostico Markdown: `{diagnosis_md}`",
        f"- Diagnostico JSON: `{diagnosis_json}`",
        "",
        "Esta es una copia auxiliar. La version canonica del estilo se guarda dentro de la carpeta del skill.",
        "",
    ]
    write(summary_md, "\n".join(summary), overwrite)
    return summary_md


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Genera perfil de estilo desde documentos modelo y compara un borrador en una sola corrida."
    )
    parser.add_argument("--model", nargs="+", required=True, help="Documento(s) modelo PDF, DOCX, HTML, TXT o Markdown.")
    parser.add_argument("--draft", required=True, help="Borrador a comparar PDF, DOCX, HTML, TXT o Markdown.")
    parser.add_argument("--style-name", help="Nombre del estilo. Se guarda en skills/humanizar-redaccion-academica/styles/<nombre>.")
    parser.add_argument("--out-dir", help="Carpeta espejo opcional. La salida canonica siempre queda dentro del skill.")
    parser.add_argument("--prefix", default="estilo", help="Prefijo de archivos de salida.")
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    if not args.prefix or any(c in args.prefix for c in '/\\\\:') or args.prefix in ('.', '..'):
        parser.error('--prefix debe ser un nombre simple, no una ruta')

    model_paths = [Path(item) for item in args.model]
    draft_path = Path(args.draft)
    missing = [str(path) for path in model_paths + [draft_path] if not path.exists()]
    if missing:
        raise SystemExit("No existen: " + ", ".join(missing))

    style_name = args.style_name or args.prefix
    style_slug = slugify(style_name)
    out_dir = skill_root() / "styles" / style_slug
    targets = [out_dir/name for name in ('perfil.md','perfil.json','diagnostico.md','diagnostico.json','resumen.md','manifest.json')]
    if args.out_dir:
        targets += [Path(args.out_dir)/f'{args.prefix}_{name}' for name in ('perfil.md','perfil.json','diagnostico.md','diagnostico.json','resumen.md')]
    try:
        validate_outputs([*model_paths, draft_path], targets, args.overwrite)
    except ValueError as exc:
        parser.error(str(exc))
    profile = profiler.build_profile(model_paths)
    with tempfile.TemporaryDirectory(prefix='perfil-') as temporary:
        temp_profile_json = Path(temporary)/'perfil.json'
        write_json(temp_profile_json, profile)
        result = comparator.compare(draft_path, temp_profile_json)
    result['profile_file'] = str(out_dir/'perfil.json')
    paths = write_canonical_outputs(out_dir, profile, result, style_name, model_paths, draft_path, args.overwrite)

    if args.out_dir:
        mirror = write_legacy_copy(Path(args.out_dir), args.prefix, profile, result, args.overwrite)
        print(f"Copia auxiliar: {mirror}")
    print(f"Estilo guardado: {paths['summary_md']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
