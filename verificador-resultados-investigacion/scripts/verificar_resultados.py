#!/usr/bin/env python3
"""Verifica cálculos mecánicos y genera informes trazables por hallazgo."""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile


SUPPORTED_TYPES = {"porcentaje", "suma", "media", "total_grupos", "consistencia"}
STATES = ("verificado", "incorrecto", "inconsistente", "no_verificable")


def is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def require_numbers(values: object, field: str) -> list[float]:
    if not isinstance(values, list) or not values or any(not is_number(value) for value in values):
        raise ValueError(f"{field} debe ser una lista no vacía de números finitos")
    return [float(value) for value in values]


def clean_number(value: float | None) -> float | None:
    if value is None:
        return None
    return round(float(value), 10)


def display(value: object) -> str:
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def validate_payload(payload: object) -> dict:
    if not isinstance(payload, dict):
        raise ValueError("La entrada debe ser un objeto JSON")
    project = payload.get("proyecto")
    if not isinstance(project, str) or not project.strip():
        raise ValueError("proyecto debe ser una cadena no vacía")
    tolerance = payload.get("tolerancia", 0.01)
    if not is_number(tolerance) or tolerance < 0:
        raise ValueError("tolerancia debe ser un número finito no negativo")
    results = payload.get("resultados")
    if not isinstance(results, list):
        raise ValueError("resultados debe ser una lista")

    seen: set[str] = set()
    for index, item in enumerate(results, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"resultado {index} debe ser un objeto")
        identifier = item.get("id")
        if not isinstance(identifier, str) or not re.fullmatch(r"[A-Za-z0-9._-]+", identifier):
            raise ValueError(f"id inválido en resultado {index}")
        if identifier in seen:
            raise ValueError(f"id duplicado: {identifier}")
        seen.add(identifier)
        if item.get("tipo") not in SUPPORTED_TYPES:
            raise ValueError(f"tipo no admitido en {identifier}: {item.get('tipo')!r}")
        for field in ("ubicacion", "afirmacion", "fuente"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                raise ValueError(f"{field} ausente o inválido en {identifier}")
        if not is_number(item.get("reportado")):
            raise ValueError(f"reportado debe ser un número finito en {identifier}")

    return {"proyecto": project.strip(), "tolerancia": float(tolerance), "resultados": results}


def base_result(item: dict) -> dict:
    return {
        "id": item["id"],
        "ubicacion": item["ubicacion"],
        "afirmacion": item["afirmacion"],
        "tipo": item["tipo"],
        "reportado": clean_number(float(item["reportado"])),
        "esperado": None,
        "diferencia": None,
        "estado": "no_verificable",
        "motivo": "",
        "verificacion": "",
        "intervencion_propuesta": "",
        "fuente": item["fuente"],
    }


def compare_calculation(result: dict, expected: float, tolerance: float, verification: str) -> dict:
    reported = float(result["reportado"])
    difference = reported - expected
    result["esperado"] = clean_number(expected)
    result["diferencia"] = clean_number(difference)
    result["verificacion"] = verification
    if math.isclose(reported, expected, rel_tol=0.0, abs_tol=tolerance):
        result["estado"] = "verificado"
        result["motivo"] = "El valor reportado coincide con el cálculo reproducido dentro de la tolerancia."
        result["intervencion_propuesta"] = "No se requiere corrección numérica."
    else:
        result["estado"] = "incorrecto"
        result["motivo"] = (
            f"El valor reportado ({display(reported)}) no coincide con el valor recalculado "
            f"({display(clean_number(expected))})."
        )
        result["intervencion_propuesta"] = (
            f"Se propone corregir el valor reportado de {display(reported)} a "
            f"{display(clean_number(expected))}, después de confirmar la fuente indicada; "
            "no se modifica automáticamente el manuscrito ni los datos."
        )
    return result


def unverifiable(result: dict, reason: str) -> dict:
    result["estado"] = "no_verificable"
    result["motivo"] = reason
    result["verificacion"] = "No fue posible reproducir el cálculo con los insumos disponibles."
    result["intervencion_propuesta"] = (
        "Recuperar la fuente o los insumos faltantes y repetir la verificación; "
        "no se propone una corrección numérica."
    )
    return result


def verify_item(item: dict, tolerance: float) -> dict:
    result = base_result(item)
    kind = item["tipo"]

    if kind == "porcentaje":
        numerator, denominator = item.get("numerador"), item.get("denominador")
        if not is_number(numerator):
            return unverifiable(result, "Falta un numerador numérico verificable.")
        if not is_number(denominator):
            return unverifiable(result, "Falta un denominador numérico verificable.")
        if float(denominator) == 0:
            return unverifiable(result, "El denominador es cero; el porcentaje no puede calcularse.")
        expected = float(numerator) / float(denominator) * 100
        verification = (
            f"{display(numerator)} / {display(denominator)} × 100 = "
            f"{display(clean_number(expected))}"
        )
        return compare_calculation(result, expected, tolerance, verification)

    if kind in {"suma", "total_grupos"}:
        field = "componentes" if kind == "suma" else "grupos"
        try:
            values = require_numbers(item.get(field), field)
        except ValueError as error:
            return unverifiable(result, str(error))
        expected = sum(values)
        verification = f"Suma de {field}: {' + '.join(display(value) for value in values)} = {display(clean_number(expected))}"
        return compare_calculation(result, expected, tolerance, verification)

    if kind == "media":
        try:
            values = require_numbers(item.get("valores"), "valores")
        except ValueError as error:
            return unverifiable(result, str(error))
        expected = sum(values) / len(values)
        verification = (
            f"Media de {len(values)} valores: {display(clean_number(sum(values)))} / "
            f"{len(values)} = {display(clean_number(expected))}"
        )
        return compare_calculation(result, expected, tolerance, verification)

    appearances = item.get("apariciones")
    if not isinstance(appearances, list) or not appearances:
        return unverifiable(result, "Faltan apariciones comparables del mismo resultado.")
    invalid = [entry for entry in appearances if not isinstance(entry, dict) or not is_number(entry.get("valor")) or not isinstance(entry.get("ubicacion"), str)]
    if invalid:
        return unverifiable(result, "Una o más apariciones carecen de ubicación o valor numérico verificable.")
    values = [float(result["reportado"]), *(float(entry["valor"]) for entry in appearances)]
    unique_values = []
    for value in values:
        if not any(math.isclose(value, known, rel_tol=0.0, abs_tol=tolerance) for known in unique_values):
            unique_values.append(value)
    result["verificacion"] = "; ".join(
        [f"{result['ubicacion']}: {display(result['reportado'])}"]
        + [f"{entry['ubicacion']}: {display(entry['valor'])}" for entry in appearances]
    )
    if len(unique_values) == 1:
        result["estado"] = "verificado"
        result["esperado"] = result["reportado"]
        result["diferencia"] = 0.0
        result["motivo"] = "Todas las apariciones comparadas coinciden dentro de la tolerancia."
        result["intervencion_propuesta"] = "No se requiere corrección numérica."
    else:
        rendered = ", ".join(display(clean_number(value)) for value in unique_values)
        result["estado"] = "inconsistente"
        result["motivo"] = f"El mismo resultado aparece con valores incompatibles: {rendered}."
        result["intervencion_propuesta"] = (
            "Contrastar cada aparición con la fuente de autoridad, identificar el valor correcto y "
            "actualizar de forma trazable todas las ubicaciones afectadas."
        )
    return result


def render_finding(result: dict) -> str:
    expected = "No determinado" if result["esperado"] is None else display(result["esperado"])
    return "\n".join(
        [
            f"# {result['id']} — {result['estado'].replace('_', ' ').title()}",
            "",
            f"- **Ubicación:** {result['ubicacion']}",
            f"- **Afirmación:** {result['afirmacion']}",
            f"- **Fuente declarada:** {result['fuente']}",
            f"- **Valor reportado:** {display(result['reportado'])}",
            f"- **Valor esperado:** {expected}",
            "",
            "## Verificación",
            "",
            result["verificacion"],
            "",
            "## Por qué está mal o no puede confirmarse",
            "",
            result["motivo"],
            "",
            "## Intervención propuesta",
            "",
            result["intervencion_propuesta"],
            "",
            "## Aprobación y aplicación",
            "",
            "Pendiente. Este informe no modifica el manuscrito ni la fuente de datos.",
            "",
        ]
    )


def render_summary(report: dict) -> str:
    lines = [
        "# Informe consolidado de verificación de resultados",
        "",
        f"- **Proyecto:** {report['proyecto']}",
        f"- **Fuente de entrada:** {report['entrada']}",
        f"- **Tolerancia absoluta:** {display(report['tolerancia'])}",
        "",
        "## Resumen",
        "",
    ]
    lines.extend(f"- **{state.replace('_', ' ').title()}:** {report['resumen'][state]}" for state in STATES)
    lines.extend(["", "## Resultados", "", "| ID | Ubicación | Tipo | Reportado | Esperado | Estado |", "| --- | --- | --- | ---: | ---: | --- |"])
    for item in report["resultados"]:
        expected = "—" if item["esperado"] is None else display(item["esperado"])
        lines.append(
            f"| {item['id']} | {item['ubicacion']} | {item['tipo']} | "
            f"{display(item['reportado'])} | {expected} | {item['estado']} |"
        )
    lines.extend(
        [
            "",
            "## Límite",
            "",
            "Este informe comprueba operaciones y consistencia interna declaradas. No certifica el diseño, la calidad de los datos, la elección del método estadístico ni la validez científica de las conclusiones.",
            "",
        ]
    )
    return "\n".join(lines)


def write_reports(output: Path, report: dict) -> None:
    if output.exists():
        raise FileExistsError(f"El directorio de salida ya existe: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{output.name}.", dir=output.parent))
    try:
        (staging / "informe-consolidado.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (staging / "informe-consolidado.md").write_text(render_summary(report), encoding="utf-8")
        findings = [item for item in report["resultados"] if item["estado"] != "verificado"]
        if findings:
            folder = staging / "hallazgos"
            folder.mkdir()
            for item in findings:
                (folder / f"{item['id']}.md").write_text(render_finding(item), encoding="utf-8")
        os.replace(staging, output)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Registro JSON de resultados")
    parser.add_argument("--out-dir", required=True, type=Path, help="Directorio nuevo para informes")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        source = args.input.resolve(strict=True)
        if not source.is_file():
            raise ValueError(f"La entrada no es un archivo: {source}")
        output = args.out_dir.resolve()
        if output == source or source in output.parents:
            raise ValueError("La salida no puede reemplazar ni contener la entrada")
        payload = validate_payload(json.loads(source.read_text(encoding="utf-8")))
        results = [verify_item(item, payload["tolerancia"]) for item in payload["resultados"]]
        summary = {state: sum(item["estado"] == state for item in results) for state in STATES}
        report = {
            "proyecto": payload["proyecto"],
            "entrada": str(source),
            "tolerancia": payload["tolerancia"],
            "resumen": summary,
            "resultados": results,
        }
        write_reports(output, report)
        print(json.dumps({"status": "ok" if not any(summary[state] for state in STATES[1:]) else "hallazgos", "out_dir": str(output), "resumen": summary}, ensure_ascii=False))
        return 0 if not any(summary[state] for state in STATES[1:]) else 1
    except (FileExistsError, json.JSONDecodeError, OSError, UnicodeError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
