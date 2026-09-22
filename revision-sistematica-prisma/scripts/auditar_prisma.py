#!/usr/bin/env python3
"""Audita conteos del flujo y cobertura documental PRISMA 2020."""

from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path
import sys
import tempfile
from typing import Any


ITEMS = (
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10a", "10b", "11", "12",
    "13a", "13b", "13c", "13d", "13e", "13f", "14", "15", "16a", "16b", "17",
    "18", "19", "20a", "20b", "20c", "20d", "21", "22", "23a", "23b", "23c",
    "23d", "24a", "24b", "24c", "25", "26", "27",
)
ALLOWED_STATUSES = {"complete", "partial", "missing", "not_applicable", "unverifiable"}
CHECKLIST_FIELDS = {"item", "status", "location", "evidence", "notes"}


class InputError(ValueError):
    """Entrada inválida que impide una auditoría fiable."""


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise InputError(f"No se pudo leer JSON válido de {path}: {error}") from error
    if not isinstance(data, dict):
        raise InputError("La raíz JSON debe ser un objeto")
    return data


def count_at(data: dict[str, Any], *parts: str) -> int:
    current: Any = data
    dotted = ".".join(parts)
    for part in parts:
        if not isinstance(current, dict) or part not in current:
            raise InputError(f"Falta el conteo requerido: {dotted}")
        current = current[part]
    if isinstance(current, bool) or not isinstance(current, int) or current < 0:
        raise InputError(f"{dotted} debe ser un entero no negativo")
    return current


def flow_report(data: dict[str, Any]) -> dict[str, Any]:
    review_type = data.get("review_type")
    if review_type not in {"new", "updated"}:
        raise InputError("review_type debe ser 'new' o 'updated'")

    databases = count_at(data, "identification", "records_databases_registers")
    duplicates = count_at(data, "removed_before_screening", "duplicates")
    automation = count_at(data, "removed_before_screening", "automation")
    other_removed = count_at(data, "removed_before_screening", "other")
    screened = count_at(data, "screening", "records_screened")
    records_excluded = count_at(data, "screening", "records_excluded")
    database_reports_sought = count_at(data, "database_path", "reports_sought")
    database_not_retrieved = count_at(data, "database_path", "reports_not_retrieved")
    database_reports_assessed = count_at(data, "database_path", "reports_assessed")
    other_identified = count_at(data, "other_methods_path", "reports_identified")
    other_reports_sought = count_at(data, "other_methods_path", "reports_sought")
    other_not_retrieved = count_at(data, "other_methods_path", "reports_not_retrieved")
    other_reports_assessed = count_at(data, "other_methods_path", "reports_assessed")
    reports_included = count_at(data, "included", "reports")
    studies_included = count_at(data, "included", "studies")

    def sum_reasons(section: str) -> int:
        reasons = data.get(section, {}).get("reports_excluded_by_reason")
        if not isinstance(reasons, dict):
            raise InputError(f"{section}.reports_excluded_by_reason debe ser un objeto")
        total = 0
        for reason, value in reasons.items():
            if not isinstance(reason, str) or not reason.strip():
                raise InputError(f"Cada razón de exclusión en {section} debe tener nombre")
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise InputError(
                    f"{section}.reports_excluded_by_reason.{reason} debe ser un entero no negativo"
                )
            total += value
        return total

    database_excluded = sum_reasons("database_path")
    other_excluded = sum_reasons("other_methods_path")
    excluded_by_reason = database_excluded + other_excluded

    identified = databases
    removed = duplicates + automation + other_removed
    expected_screened = identified - removed
    expected_database_sought = screened - records_excluded
    expected_database_assessed = database_reports_sought - database_not_retrieved
    expected_other_assessed = other_reports_sought - other_not_retrieved
    expected_included_reports = (
        database_reports_assessed
        + other_reports_assessed
        - database_excluded
        - other_excluded
    )

    checks: list[dict[str, Any]] = []

    def add_check(name: str, actual: int, expected: int, equation: str) -> None:
        checks.append(
            {
                "name": name,
                "actual": actual,
                "expected": expected,
                "equation": equation,
                "ok": actual == expected,
            }
        )

    add_check(
        "records_screened",
        screened,
        expected_screened,
        f"{identified} - {removed} = {expected_screened}",
    )
    add_check(
        "reports_sought",
        database_reports_sought,
        expected_database_sought,
        f"{screened} - {records_excluded} = {expected_database_sought}",
    )
    add_check(
        "database_path.reports_assessed",
        database_reports_assessed,
        expected_database_assessed,
        f"{database_reports_sought} - {database_not_retrieved} = {expected_database_assessed}",
    )
    add_check(
        "other_methods_path.reports_sought",
        other_reports_sought,
        other_identified,
        f"{other_identified} informes identificados = {other_identified} buscados",
    )
    add_check(
        "other_methods_path.reports_assessed",
        other_reports_assessed,
        expected_other_assessed,
        f"{other_reports_sought} - {other_not_retrieved} = {expected_other_assessed}",
    )
    add_check(
        "included.reports",
        reports_included,
        expected_included_reports,
        (
            f"({database_reports_assessed} + {other_reports_assessed}) - "
            f"({database_excluded} + {other_excluded}) = {expected_included_reports}"
        ),
    )
    if studies_included > reports_included:
        checks.append(
            {
                "name": "included.studies",
                "actual": studies_included,
                "expected": f"<= {reports_included}",
                "equation": "un estudio puede tener uno o más informes",
                "ok": False,
            }
        )

    return {
        "status": "PASS" if all(check["ok"] for check in checks) else "INCONSISTENT",
        "review_type": review_type,
        "derived": {
            "identified_records": identified,
            "reports_identified_other_methods": other_identified,
            "removed_before_screening": removed,
            "reports_excluded_with_reasons": excluded_by_reason,
            "reports_included": reports_included,
            "studies_included": studies_included,
        },
        "checks": checks,
        "note": "La aritmética coherente no certifica decisiones metodológicas ni cumplimiento PRISMA.",
    }


def checklist_report(path: Path) -> dict[str, Any]:
    try:
        handle = path.open("r", encoding="utf-8-sig", newline="")
    except (OSError, UnicodeError) as error:
        raise InputError(f"No se pudo leer {path}: {error}") from error
    with handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or not CHECKLIST_FIELDS.issubset(reader.fieldnames):
            raise InputError("El CSV requiere columnas: item,status,location,evidence,notes")
        rows: dict[str, dict[str, str]] = {}
        for line_number, raw in enumerate(reader, start=2):
            row = {key: (raw.get(key) or "").strip() for key in CHECKLIST_FIELDS}
            item = row["item"]
            if item not in ITEMS:
                raise InputError(f"Ítem desconocido en línea {line_number}: {item or '[vacío]'}")
            if item in rows:
                raise InputError(f"Ítem duplicado en línea {line_number}: {item}")
            if row["status"] not in ALLOWED_STATUSES:
                raise InputError(f"Estado inválido para {item}: {row['status'] or '[vacío]'}")
            if row["status"] == "complete" and (not row["location"] or not row["evidence"]):
                raise InputError(f"El ítem completo {item} requiere location y evidence")
            if row["status"] == "not_applicable" and not row["notes"]:
                raise InputError(f"El ítem no aplicable {item} requiere justificación en notes")
            rows[item] = row

    missing_items = [item for item in ITEMS if item not in rows]
    counts = {status: 0 for status in sorted(ALLOWED_STATUSES)}
    for row in rows.values():
        counts[row["status"]] += 1
    unresolved = [
        item
        for item, row in rows.items()
        if row["status"] in {"partial", "missing", "unverifiable"}
    ]
    status = "PASS" if not missing_items and not unresolved else "INCOMPLETE"
    return {
        "status": status,
        "counts": counts,
        "absent_items": missing_items,
        "unresolved_items": unresolved,
        "not_applicable_items": [
            item for item, row in rows.items() if row["status"] == "not_applicable"
        ],
        "note": "La matriz registra cobertura documental; no evalúa por sí sola rigor ni veracidad.",
    }


def atomic_write_json(path: Path, data: dict[str, Any], overwrite: bool) -> None:
    path = path.resolve()
    if path.exists() and not overwrite:
        raise InputError(f"La salida ya existe: {path}; use --overwrite para reemplazarla")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
        ) as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
            temporary = Path(handle.name)
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def print_flow(report: dict[str, Any]) -> None:
    print(report["status"])
    for check in report["checks"]:
        marker = "OK" if check["ok"] else "ERROR"
        print(
            f"{marker} {check['name']}: actual={check['actual']}; "
            f"esperado={check['expected']} ({check['equation']})"
        )


def print_checklist(report: dict[str, Any]) -> None:
    counts = report["counts"]
    print(report["status"])
    print(
        " ".join(
            f"{status}={counts[status]}"
            for status in ("complete", "not_applicable", "partial", "missing", "unverifiable")
        )
    )
    if report["absent_items"]:
        print("Ítems ausentes: " + ", ".join(report["absent_items"]))
    if report["unresolved_items"]:
        print("Ítems no resueltos: " + ", ".join(report["unresolved_items"]))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Audita aritmética del flujo y cobertura documental PRISMA 2020."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("flow-check", "checklist-audit"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("--input", required=True, type=Path)
        subparser.add_argument("--out", type=Path)
        subparser.add_argument("--overwrite", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "flow-check":
            report = flow_report(read_json(args.input))
            print_flow(report)
        else:
            report = checklist_report(args.input)
            print_checklist(report)
        if args.out is not None:
            atomic_write_json(args.out, report, args.overwrite)
        return 0 if report["status"] == "PASS" else 1
    except InputError as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
