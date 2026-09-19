#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'workflow-maestro-academico-editorial/scripts'))
from archivos_seguros import atomic_write, validate_outputs
from typing import Any

import documento_a_perfil_estilo as profiler


def load_profile(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8", errors="replace"))


def compare_stats(current: dict[str, Any], target: dict[str, Any]) -> list[str]:
    notes = []
    cur_avg = float(current["sentence_stats"].get("avg", 0))
    tgt_avg = float(target["sentence_stats"].get("avg", 0))
    cur_stdev = float(current["sentence_stats"].get("stdev", 0))
    tgt_stdev = float(target["sentence_stats"].get("stdev", 0))
    if tgt_avg and abs(cur_avg - tgt_avg) >= 6:
        if cur_avg > tgt_avg:
            notes.append(f"Las oraciones del borrador son mas largas que el perfil ({cur_avg} vs {tgt_avg} palabras).")
        else:
            notes.append(f"Las oraciones del borrador son mas breves que el perfil ({cur_avg} vs {tgt_avg} palabras).")
    if tgt_stdev and cur_stdev < max(5, tgt_stdev * 0.65):
        notes.append("El borrador tiene menos variacion de ritmo que el perfil; alternar oraciones medias con cierres breves.")
    if tgt_stdev and cur_stdev > tgt_stdev * 1.6:
        notes.append("El borrador fluctua mas que el perfil; revisar frases excesivamente largas o fragmentadas.")
    return notes


def phrase_map(items: list[dict[str, Any]]) -> dict[str, int]:
    return {str(item["phrase"]): int(item["count"]) for item in items}


def compare_phrases(current: dict[str, Any], target: dict[str, Any], key: str) -> list[str]:
    cur = phrase_map(current.get(key, []))
    tgt = phrase_map(target.get(key, []))
    notes = []
    for phrase, count in sorted(cur.items(), key=lambda item: (-item[1], item[0])):
        target_count = tgt.get(phrase, 0)
        if count >= 3 and (not target_count or count > target_count * 2):
            notes.append(f"`{phrase}` aparece {count} veces y domina mas que en el perfil.")
    missing = [phrase for phrase, count in tgt.items() if count >= 2 and cur.get(phrase, 0) == 0]
    if missing:
        notes.append("El borrador no usa algunos recursos frecuentes del perfil: " + ", ".join(f"`{item}`" for item in missing[:6]) + ".")
    return notes


def protected_warning(profile: dict[str, Any]) -> list[str]:
    protected = profile.get("protected_content", {})
    total = sum(int(v) for v in protected.values() if isinstance(v, int))
    if total:
        return [f"Hay {total} elementos protegidos; no reescribir citas, DOI, URL, tablas, codigo ni referencias."]
    return []


def build_edit_brief(current: dict[str, Any], target: dict[str, Any], notes: list[str]) -> list[str]:
    brief = [
        "Reescribir por secciones cortas y verificar citas despues de cada bloque.",
        "Conservar la tesis del parrafo; cambiar entrada, ritmo o transicion solo si aporta naturalidad.",
        "No copiar frases del documento modelo; usar el perfil como patron de ritmo y criterio.",
    ]
    if any("menos variacion" in note for note in notes):
        brief.append("Insertar una oracion breve de cierre despues de explicaciones densas, o dividir una oracion larga en dos con relacion logica clara.")
    if any("domina mas" in note for note in notes):
        brief.append("Sustituir conectores repetidos por relaciones especificas: causa, contraste, consecuencia, ejemplo o condicion.")
    current_avg = current["paragraph_stats"].get("avg", 0)
    target_avg = target["paragraph_stats"].get("avg", 0)
    if current_avg > target_avg + 35:
        brief.append("Reducir parrafos demasiado extensos o insertar una transicion interna.")
    return brief


def compare(target_text_path: Path, profile_path: Path) -> dict[str, Any]:
    target_profile = load_profile(profile_path)
    current_profile = profiler.build_profile([target_text_path])
    notes = []
    notes.extend(compare_stats(current_profile, target_profile))
    notes.extend(compare_phrases(current_profile, target_profile, "connectors"))
    notes.extend(compare_phrases(current_profile, target_profile, "hedges"))
    notes.extend(protected_warning(current_profile))
    if not notes:
        notes.append("El borrador esta razonablemente alineado con el perfil; aplicar solo revision fina.")
    return {
        "target_file": str(target_text_path),
        "profile_file": str(profile_path),
        "current_summary": {
            "counts": current_profile["counts"],
            "sentence_stats": current_profile["sentence_stats"],
            "paragraph_stats": current_profile["paragraph_stats"],
            "connectors": current_profile["connectors"][:10],
            "hedges": current_profile["hedges"][:10],
            "protected_content": current_profile["protected_content"],
        },
        "profile_summary": {
            "sentence_stats": target_profile["sentence_stats"],
            "paragraph_stats": target_profile["paragraph_stats"],
            "connectors": target_profile.get("connectors", [])[:10],
            "hedges": target_profile.get("hedges", [])[:10],
        },
        "diagnosis": notes,
        "edit_brief": build_edit_brief(current_profile, target_profile, notes),
        "note": "Este comparador no detecta IA ni garantiza resultados ante detectores; orienta revision editorial.",
    }


def render(result: dict[str, Any]) -> str:
    lines = [
        "# Comparacion con perfil de estilo",
        "",
        f"- Borrador: `{result['target_file']}`",
        f"- Perfil: `{result['profile_file']}`",
        "",
        "## Diagnostico",
        "",
    ]
    lines.extend(f"- {item}" for item in result["diagnosis"])
    lines.extend(["", "## Instrucciones de reescritura", ""])
    lines.extend(f"- {item}" for item in result["edit_brief"])
    lines.extend(["", "## Resumen del borrador", ""])
    lines.append(f"- Oraciones: {result['current_summary']['sentence_stats']}")
    lines.append(f"- Parrafos: {result['current_summary']['paragraph_stats']}")
    lines.append(f"- Contenido protegido: {result['current_summary']['protected_content']}")
    lines.extend(["", "## Nota", "", result["note"], ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Compara un borrador contra un perfil de estilo JSON.")
    parser.add_argument("input", help="Borrador PDF, DOCX, HTML, TXT o Markdown.")
    parser.add_argument("--profile", required=True, help="perfil.json generado por documento_a_perfil_estilo.py")
    parser.add_argument("--out", help="Salida Markdown.")
    parser.add_argument("--json-out", help="Salida JSON.")
    parser.add_argument('--overwrite', action='store_true', help='Reemplazar informes existentes, nunca entradas')
    args = parser.parse_args()
    try:
        validate_outputs([args.input, args.profile], [args.out, args.json_out], args.overwrite)
    except ValueError as exc:
        parser.error(str(exc))
    result = compare(Path(args.input), Path(args.profile))
    report = render(result)
    if args.out:
        atomic_write(args.out, report, overwrite=args.overwrite)
    else:
        print(report, end="")
    if args.json_out:
        atomic_write(args.json_out, json.dumps(result, ensure_ascii=False, indent=2), overwrite=args.overwrite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
