#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import shutil
import sys
import zipfile
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'editor-en-jefe/scripts'))
from archivos_seguros import atomic_write, atomic_output, validate_outputs


PHASES = [
    "planificacion",
    "preguntas",
    "protocolo",
    "busqueda",
    "snowballing",
    "seleccion",
    "fuentes",
    "calidad",
    "extraccion",
    "sintesis",
    "informe",
    "auditoria",
]

DEFAULT_EXPECTED_THRESHOLDS = {
    "unique_records": 300,
    "full_texts_assessed": 100,
    "included_studies": 50,
    "recent_window_years": 5,
    "recent_evidence_percentage": 60.0,
    "enforcement": "advisory",
    "external_requirement_source": "",
}

DEFAULT_SOURCE_STRATEGY = {
    "recommended_main_sources_min": 4,
    "recommended_main_sources_max": 5,
    "seed_articles_recommended_min": 5,
    "seed_articles_recommended_max": 10,
    "seed_recovery_target_percentage": 90.0,
    "marginal_contribution_warning_percentage": 1.0,
    "seed_articles_unavailable": False,
    "seed_unavailability_justification": "",
}

DEFAULT_SEARCH_UPDATE = {
    "recommended_max_age_days": 90,
    "enforcement": "advisory",
    "require_update_before_submission": True,
    "external_requirement_source": "",
}

DEFAULT_FULLTEXT_POLICY = {
    "enforcement": "mandatory",
    "require_local_fulltext_for_use": True,
    "require_content_review": True,
    "require_citation_review": True,
    "inaccessible_decision": "excluded",
    "exclusion_code": "FT-NO-DESCARGADO",
    "allow_exception": False,
}

SOURCE_TYPES = {
    "bibliographic_database",
    "citation_index",
    "specialized_digital_library",
    "publisher_platform",
    "academic_search_engine",
    "repository",
    "complementary_source",
}

SOURCE_ROLES = {
    "multidisciplinary",
    "domain_specialized",
    "independent_complement",
    "supporting",
}

DIRECTORIES = [
    "00_gestion/01_configuracion",
    "00_gestion/02_planificacion",
    "00_gestion/03_seguimiento",
    "00_gestion/04_inventario",
    "00_gestion/05_decisiones",
    "00_gestion/06_riesgos",
    "00_gestion/07_cronograma",
    "00_gestion/08_excepciones",
    "01_protocolo/01_vigente",
    "01_protocolo/02_versiones",
    "01_protocolo/03_pilotos/01_busqueda",
    "01_protocolo/03_pilotos/02_seleccion",
    "01_protocolo/03_pilotos/03_calidad",
    "01_protocolo/03_pilotos/04_extraccion",
    "01_protocolo/04_aprobaciones",
    "02_busquedas/01_fuentes",
    "02_busquedas/02_cadenas/01_borradores",
    "02_busquedas/02_cadenas/02_definitivas",
    "02_busquedas/03_registro",
    "02_busquedas/04_resultados/01_brutos",
    "02_busquedas/04_resultados/02_normalizados",
    "02_busquedas/05_articulos-semilla",
    "02_busquedas/06_busqueda-manual",
    "02_busquedas/07_literatura-gris",
    "02_busquedas/08_actualizaciones",
    "02_busquedas/09_aporte-marginal",
    "02_busquedas/10_saturacion",
    "02_busquedas/11_logs",
    "03_seleccion/01_registro-maestro",
    "03_seleccion/02_deduplicacion",
    "03_seleccion/03_cribado-titulo-resumen",
    "03_seleccion/04_cribado-texto-completo",
    "03_seleccion/05_desacuerdos",
    "03_seleccion/06_snowballing",
    "03_seleccion/07_impacto-novedad",
    "04_fuentes/01_originales/01_incluidos",
    "04_fuentes/01_originales/02_excluidos",
    "04_fuentes/01_originales/03_pendientes",
    "04_fuentes/02_suplementos/01_incluidos",
    "04_fuentes/02_suplementos/02_excluidos",
    "04_fuentes/02_suplementos/03_pendientes",
    "04_fuentes/03_procesados/01_markdown",
    "04_fuentes/03_procesados/02_texto",
    "04_fuentes/03_procesados/03_segmentos",
    "04_fuentes/04_metadatos",
    "04_fuentes/05_inaccesibles",
    "04_fuentes/06_cuarentena",
    "05_calidad/01_instrumentos",
    "05_calidad/02_piloto",
    "05_calidad/03_evaluaciones/01_revisor-1",
    "05_calidad/03_evaluaciones/02_revisor-2",
    "05_calidad/04_resoluciones",
    "05_calidad/05_sensibilidad",
    "06_extraccion/01_formularios",
    "06_extraccion/02_piloto",
    "06_extraccion/03_individual",
    "06_extraccion/04_verificacion",
    "06_extraccion/05_consolidado",
    "07_sintesis/01_descriptiva",
    "07_sintesis/02_narrativa",
    "07_sintesis/03_tematica",
    "07_sintesis/04_cuantitativa",
    "07_sintesis/05_heterogeneidad",
    "07_sintesis/06_sensibilidad",
    "07_sintesis/07_brechas-novedad",
    "07_sintesis/08_tablas",
    "07_sintesis/09_graficos",
    "07_sintesis/10_trazabilidad",
    "08_informe/01_borradores",
    "08_informe/02_final",
    "08_informe/03_referencias",
    "08_informe/04_anexos",
    "08_informe/05_material-suplementario",
    "08_informe/06_envio",
    "09_auditorias/01_integridad",
    "09_auditorias/02_cobertura",
    "09_auditorias/03_metodologia",
    "09_auditorias/04_citas",
    "09_auditorias/05_entrega",
    "10_respaldo/01_manifiestos",
    "10_respaldo/02_snapshots",
    "10_respaldo/03_logs",
    "10_respaldo/04_recuperacion",
    "10_respaldo/05_otros",
    "11_entrega/01_manuscrito",
    "11_entrega/02_matrices",
    "11_entrega/03_fuentes",
    "11_entrega/04_paquete-reproducible",
]

TEMPLATES = {
    "plan.md": "00_gestion/02_planificacion/00-02_plan.md",
    "criterios-cobertura-impacto.md": (
        "00_gestion/02_planificacion/00-02_criterios-cobertura-impacto.md"
    ),
    "excepciones-metodologicas.csv": (
        "00_gestion/08_excepciones/00-08_excepciones-metodologicas.csv"
    ),
    "protocolo.md": "01_protocolo/01_vigente/01-01_protocolo.md",
    "evaluacion-protocolo.md": (
        "01_protocolo/01_vigente/01-01_evaluacion-protocolo.md"
    ),
    "desviaciones.csv": "01_protocolo/02_versiones/01-02_desviaciones.csv",
    "registro-busquedas.csv": (
        "02_busquedas/03_registro/02-03_registro-busquedas.csv"
    ),
    "fuentes-consultadas.csv": (
        "02_busquedas/01_fuentes/02-01_fuentes-consultadas.csv"
    ),
    "fuentes-no-consultadas.csv": (
        "02_busquedas/01_fuentes/02-01_fuentes-no-consultadas.csv"
    ),
    "articulos-semilla.csv": (
        "02_busquedas/05_articulos-semilla/02-05_articulos-semilla.csv"
    ),
    "aporte-marginal-fuentes.csv": (
        "02_busquedas/09_aporte-marginal/02-09_aporte-marginal-fuentes.csv"
    ),
    "evaluacion-saturacion.csv": (
        "02_busquedas/10_saturacion/02-10_evaluacion-saturacion.csv"
    ),
    "registros-maestros.csv": (
        "03_seleccion/01_registro-maestro/03-01_registros-maestros.csv"
    ),
    "cribado.csv": (
        "03_seleccion/03_cribado-titulo-resumen/03-03_cribado.csv"
    ),
    "exclusiones-texto-completo.csv": (
        "03_seleccion/04_cribado-texto-completo/"
        "03-04_exclusiones-texto-completo.csv"
    ),
    "snowballing.csv": "03_seleccion/06_snowballing/03-06_snowballing.csv",
    "matriz-impacto-novedad.csv": (
        "03_seleccion/07_impacto-novedad/03-07_matriz-impacto-novedad.csv"
    ),
    "fuentes-usadas.csv": (
        "04_fuentes/04_metadatos/04-04_fuentes-usadas.csv"
    ),
    "fuentes-inaccesibles.csv": (
        "04_fuentes/05_inaccesibles/04-05_fuentes-inaccesibles.csv"
    ),
    "instrumento-calidad.md": (
        "05_calidad/01_instrumentos/05-01_instrumento-calidad.md"
    ),
    "evaluacion-calidad.csv": (
        "05_calidad/03_evaluaciones/05-03_evaluacion-calidad.csv"
    ),
    "formulario-extraccion.md": (
        "06_extraccion/01_formularios/06-01_formulario-extraccion.md"
    ),
    "datos-extraidos.csv": (
        "06_extraccion/05_consolidado/06-05_datos-extraidos.csv"
    ),
    "distribucion-temporal.csv": (
        "07_sintesis/01_descriptiva/07-01_distribucion-temporal.csv"
    ),
    "mapa-evidencia.csv": (
        "07_sintesis/10_trazabilidad/07-10_mapa-evidencia.csv"
    ),
    "matriz-brechas-novedad.csv": (
        "07_sintesis/07_brechas-novedad/07-07_matriz-brechas-novedad.csv"
    ),
    "manuscrito.md": "08_informe/01_borradores/08-01_manuscrito.md",
    "auditoria-busqueda.md": (
        "09_auditorias/03_metodologia/09-03_auditoria-busqueda.md"
    ),
    "auditoria-citas.csv": (
        "09_auditorias/04_citas/09-04_auditoria-citas.csv"
    ),
}

PROJECT_PATHS = {
    "config": "00_gestion/01_configuracion/00-01_config.json",
    "plan": "00_gestion/02_planificacion/00-02_plan.md",
    "state": "00_gestion/03_seguimiento/00-03_estado.json",
    "log": "00_gestion/03_seguimiento/00-03_bitacora.csv",
    "inventory": "00_gestion/04_inventario/00-04_inventario-archivos.csv",
    "exceptions": (
        "00_gestion/08_excepciones/00-08_excepciones-metodologicas.csv"
    ),
    "protocol": "01_protocolo/01_vigente/01-01_protocolo.md",
    "search_registry": "02_busquedas/03_registro/02-03_registro-busquedas.csv",
    "consulted_sources": (
        "02_busquedas/01_fuentes/02-01_fuentes-consultadas.csv"
    ),
    "unconsulted_sources": (
        "02_busquedas/01_fuentes/02-01_fuentes-no-consultadas.csv"
    ),
    "seed_articles": (
        "02_busquedas/05_articulos-semilla/02-05_articulos-semilla.csv"
    ),
    "marginal": (
        "02_busquedas/09_aporte-marginal/02-09_aporte-marginal-fuentes.csv"
    ),
    "saturation": (
        "02_busquedas/10_saturacion/02-10_evaluacion-saturacion.csv"
    ),
    "master_records": (
        "03_seleccion/01_registro-maestro/03-01_registros-maestros.csv"
    ),
    "screening": (
        "03_seleccion/03_cribado-titulo-resumen/03-03_cribado.csv"
    ),
    "fulltext_exclusions": (
        "03_seleccion/04_cribado-texto-completo/"
        "03-04_exclusiones-texto-completo.csv"
    ),
    "snowballing": "03_seleccion/06_snowballing/03-06_snowballing.csv",
    "impact": (
        "03_seleccion/07_impacto-novedad/03-07_matriz-impacto-novedad.csv"
    ),
    "used_sources": "04_fuentes/04_metadatos/04-04_fuentes-usadas.csv",
    "quality": "05_calidad/03_evaluaciones/05-03_evaluacion-calidad.csv",
    "extraction": "06_extraccion/05_consolidado/06-05_datos-extraidos.csv",
    "temporal": (
        "07_sintesis/01_descriptiva/07-01_distribucion-temporal.csv"
    ),
    "evidence_map": (
        "07_sintesis/10_trazabilidad/07-10_mapa-evidencia.csv"
    ),
    "gaps": (
        "07_sintesis/07_brechas-novedad/07-07_matriz-brechas-novedad.csv"
    ),
    "manuscript": "08_informe/01_borradores/08-01_manuscrito.md",
    "citation_audit": "09_auditorias/04_citas/09-04_auditoria-citas.csv",
}

BITACORA_FIELDS = ["timestamp", "phase", "status", "actor", "action", "note"]
INVENTORY_FIELDS = [
    "record_id",
    "registered_at",
    "kind",
    "decision",
    "source_id",
    "study_id",
    "source_role",
    "database",
    "query_id",
    "origin",
    "title",
    "doi",
    "url",
    "original_name",
    "source_path",
    "stored_path",
    "size_bytes",
    "sha256",
    "download_status",
    "content_reviewed",
    "citations_reviewed",
    "reviewed_by",
    "reviewed_at",
    "exclusion_reason",
]
MASTER_FIELDS = [
    "study_id",
    "title",
    "authors",
    "year",
    "doi",
    "url",
    "source_database",
    "source_query",
    "document_type",
    "language",
    "duplicate_of",
    "status",
    "fulltext_record_id",
    "fulltext_path",
    "fulltext_sha256",
    "download_status",
    "content_reviewed",
    "citations_reviewed",
    "reviewed_by",
    "reviewed_at",
    "notes",
]
USED_SOURCE_FIELDS = [
    "source_id",
    "study_id",
    "reference_key",
    "source_role",
    "title",
    "doi",
    "url",
    "inventory_record_id",
    "stored_path",
    "sha256",
    "download_status",
    "content_reviewed",
    "citations_reviewed",
    "reviewed_by",
    "reviewed_at",
    "usage_status",
    "exclusion_reason",
    "notes",
]
EXCEPTION_FIELDS = [
    "exception_id",
    "date",
    "responsible",
    "threshold",
    "expected",
    "obtained",
    "audit_completed",
    "reviews_performed",
    "changes_applied",
    "justification",
    "risk",
    "impact",
    "decision",
    "approved_by",
    "status",
]
MARGINAL_FIELDS = [
    "source_id",
    "source_name",
    "raw_records",
    "duplicate_records",
    "unique_new_records",
    "screened_records",
    "included_records",
    "exclusive_included_records",
    "exclusive_included_percentage",
    "calculated_at",
    "notes",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def now_stamp() -> str:
    return datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    atomic_write(path,
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        overwrite=True,
    )


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, Any]]) -> None:
    with io.StringIO(newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})
        atomic_write(path, stream.getvalue(), overwrite=True)


def ensure_csv(path: Path, fields: list[str]) -> None:
    if not path.exists():
        write_csv(path, fields, [])
        return
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        current_fields = reader.fieldnames or []
        rows = list(reader)
    if current_fields != fields:
        write_csv(path, fields, rows)


def append_csv(path: Path, fields: list[str], row: dict[str, Any]) -> None:
    rows = read_csv(path)
    rows.append(row)
    write_csv(path, fields, rows)


def upsert_csv(
    path: Path,
    fields: list[str],
    key: str,
    row: dict[str, Any],
    preserve_finalized: bool = False,
) -> None:
    rows = read_csv(path)
    output: list[dict[str, Any]] = []
    replaced = False
    for current in rows:
        if current.get(key) != str(row.get(key, "")):
            output.append(current)
            continue
        if preserve_finalized and normalized(current.get("status")) == "finalized":
            output.append(current)
        else:
            output.append(row)
        replaced = True
    if not replaced:
        output.append(row)
    write_csv(path, fields, output)


def normalized(value: Any) -> str:
    return str(value or "").strip().casefold()


def is_true(value: Any) -> bool:
    return normalized(value) in {"1", "true", "yes", "y", "si", "sí", "executed"}


def split_multi(value: Any) -> list[str]:
    return [
        item.strip()
        for item in re.split(r"[;,|]", str(value or ""))
        if item.strip()
    ]


def number(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_name(value: Any, fallback: str = "sin-nombre") -> str:
    clean = re.sub(r"[^\w.-]+", "-", str(value).strip(), flags=re.UNICODE)
    clean = re.sub(r"-{2,}", "-", clean).strip("-._")
    return clean or fallback


def append_log(
    root: Path,
    phase: str,
    status: str,
    action: str,
    note: str = "",
    actor: str = "Codex",
) -> None:
    append_csv(
        root / PROJECT_PATHS["log"],
        BITACORA_FIELDS,
        {
            "timestamp": now_iso(),
            "phase": phase,
            "status": status,
            "actor": actor,
            "action": action,
            "note": note,
        },
    )


def require_project(root: Path) -> Path:
    root = root.resolve()
    if not (root / PROJECT_PATHS["config"]).exists():
        raise SystemExit(f"No es un proyecto Kitchenham inicializado: {root}")
    for path in root.rglob('*'):
        if path.is_symlink() or (hasattr(path, 'is_junction') and path.is_junction()):
            raise ValueError(f'No se admiten enlaces internos en el proyecto: {path}')
    return root


def copy_source(source: Path, destination: Path) -> None:
    """Copiar contenido sin sustituir destinos existentes ni publicar parciales."""
    validate_outputs([source], [destination])
    with source.open('rb') as origin, atomic_output(destination) as output:
        shutil.copyfileobj(origin, output)


def render_template(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def parse_iso_date(value: Any) -> date | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).date()
    except ValueError:
        try:
            return date.fromisoformat(text[:10])
        except ValueError:
            return None


def effective_config(config: dict[str, Any]) -> dict[str, Any]:
    result = dict(config)
    expected = dict(DEFAULT_EXPECTED_THRESHOLDS)
    if config.get("expected_thresholds"):
        expected.update(config["expected_thresholds"])
    elif config.get("coverage_thresholds"):
        legacy = config["coverage_thresholds"]
        recent = number(legacy.get("min_recent_share"), 0.60)
        expected.update(
            {
                "unique_records": legacy.get(
                    "min_candidates_after_dedup", expected["unique_records"]
                ),
                "full_texts_assessed": legacy.get(
                    "min_fulltexts_assessed", expected["full_texts_assessed"]
                ),
                "included_studies": legacy.get(
                    "min_included_studies", expected["included_studies"]
                ),
                "recent_window_years": legacy.get(
                    "recent_window_years", expected["recent_window_years"]
                ),
                "recent_evidence_percentage": recent * 100 if recent <= 1 else recent,
                "enforcement": "advisory",
            }
        )
    result["expected_thresholds"] = expected
    result["source_strategy"] = {
        **DEFAULT_SOURCE_STRATEGY,
        **config.get("source_strategy", {}),
    }
    result["search_update"] = {
        **DEFAULT_SEARCH_UPDATE,
        **config.get("search_update", {}),
    }
    result["search_audit"] = {
        "completed": False,
        "decision": "",
        "reviewed_by": "",
        "review_notes": "",
        "updated_at": None,
        **config.get("search_audit", {}),
    }
    result["fulltext_policy"] = {
        **DEFAULT_FULLTEXT_POLICY,
        **config.get("fulltext_policy", {}),
    }
    return result


def validate_configuration(
    expected: dict[str, Any],
    source_strategy: dict[str, Any],
    search_update: dict[str, Any],
) -> None:
    for key in [
        "unique_records",
        "full_texts_assessed",
        "included_studies",
        "recent_window_years",
    ]:
        if int(expected[key]) <= 0:
            raise SystemExit(f"La referencia {key} debe ser mayor que cero.")
    if not 0 < number(expected["recent_evidence_percentage"]) <= 100:
        raise SystemExit("--expected-recent-percentage debe estar entre 0 y 100.")
    if expected["enforcement"] not in {"advisory", "external_requirement"}:
        raise SystemExit("Aplicación de umbrales no válida.")
    if (
        expected["enforcement"] == "external_requirement"
        and not str(expected.get("external_requirement_source", "")).strip()
    ):
        raise SystemExit(
            "Un requisito externo exige --requirement-source con la autoridad aplicable."
        )

    minimum = int(source_strategy["recommended_main_sources_min"])
    maximum = int(source_strategy["recommended_main_sources_max"])
    if minimum <= 0 or maximum < minimum:
        raise SystemExit("El rango recomendado de fuentes es inválido.")
    seed_minimum = int(source_strategy["seed_articles_recommended_min"])
    seed_maximum = int(source_strategy["seed_articles_recommended_max"])
    if seed_minimum <= 0 or seed_maximum < seed_minimum:
        raise SystemExit("El rango recomendado de artículos semilla es inválido.")
    if not 0 < number(source_strategy["seed_recovery_target_percentage"]) <= 100:
        raise SystemExit("--seed-recovery-target debe estar entre 0 y 100.")
    if (
        source_strategy.get("seed_articles_unavailable")
        and len(
            str(source_strategy.get("seed_unavailability_justification", "")).strip()
        )
        < 30
    ):
        raise SystemExit(
            "Si no existen artículos semilla, justificarlo con al menos 30 caracteres."
        )

    if int(search_update["recommended_max_age_days"]) <= 0:
        raise SystemExit("--recommended-search-age-days debe ser mayor que cero.")
    if search_update["enforcement"] not in {"advisory", "external_requirement"}:
        raise SystemExit("Aplicación de actualización de búsqueda no válida.")
    if (
        search_update["enforcement"] == "external_requirement"
        and not str(search_update.get("external_requirement_source", "")).strip()
    ):
        raise SystemExit(
            "Una actualización exigida externamente requiere --requirement-source."
        )


def create_project(args: argparse.Namespace) -> int:
    root = Path(args.project_dir).resolve()
    if root.exists() and any(root.iterdir()):
        raise SystemExit(
            f"El directorio ya existe y no está vacío: {root}. "
            "Use otro directorio o continúe el proyecto existente."
        )

    recent_percentage = args.expected_recent_percentage
    if 0 < recent_percentage <= 1:
        recent_percentage *= 100
    expected = {
        "unique_records": args.expected_unique_records,
        "full_texts_assessed": args.expected_fulltexts,
        "included_studies": args.expected_included,
        "recent_window_years": args.recent_years,
        "recent_evidence_percentage": recent_percentage,
        "enforcement": args.threshold_enforcement,
        "external_requirement_source": args.requirement_source,
    }
    source_strategy = {
        "recommended_main_sources_min": args.recommended_sources_min,
        "recommended_main_sources_max": args.recommended_sources_max,
        "seed_articles_recommended_min": args.seed_articles_min,
        "seed_articles_recommended_max": args.seed_articles_max,
        "seed_recovery_target_percentage": args.seed_recovery_target,
        "marginal_contribution_warning_percentage": (
            args.marginal_warning_percentage
        ),
        "seed_articles_unavailable": args.seed_articles_unavailable,
        "seed_unavailability_justification": (
            args.seed_unavailability_justification
        ),
    }
    search_update = {
        "recommended_max_age_days": args.recommended_search_age_days,
        "enforcement": args.search_update_enforcement,
        "require_update_before_submission": True,
        "external_requirement_source": args.requirement_source,
    }
    validate_configuration(expected, source_strategy, search_update)

    root.mkdir(parents=True, exist_ok=True)
    for relative in DIRECTORIES:
        (root / relative).mkdir(parents=True, exist_ok=True)

    assets = Path(__file__).resolve().parent.parent / "assets"
    created_at = now_iso()
    values = {
        "TITLE": args.title,
        "TOPIC": args.topic,
        "QUESTION": args.question,
        "CITATION_STYLE": args.citation_style,
        "CREATED_AT": created_at,
    }
    for source_name, destination in TEMPLATES.items():
        target = root / destination
        target.parent.mkdir(parents=True, exist_ok=True)
        text = (assets / source_name).read_text(encoding="utf-8")
        atomic_write(target, render_template(text, values))

    config = {
        "schema_version": 4,
        "methodology": "Kitchenham y Charters (2007)",
        "methodology_exclusive": True,
        "title": args.title,
        "topic": args.topic,
        "primary_question": args.question,
        "citation_style": args.citation_style,
        "year_start": args.year_start,
        "year_end": args.year_end,
        "languages": [
            item.strip() for item in args.languages.split(";") if item.strip()
        ],
        "disciplines": [
            item.strip() for item in args.disciplines.split(";") if item.strip()
        ],
        "planned_databases": [
            item.strip() for item in args.databases.split(";") if item.strip()
        ],
        "expected_thresholds": expected,
        "source_strategy": source_strategy,
        "search_update": search_update,
        "fulltext_policy": dict(DEFAULT_FULLTEXT_POLICY),
        "search_audit": {
            "completed": False,
            "decision": "",
            "reviewed_by": "",
            "review_notes": "",
            "updated_at": None,
        },
        "created_at": created_at,
        "project_root": str(root),
    }
    write_json(root / PROJECT_PATHS["config"], config)

    state = {
        "methodology": "Kitchenham",
        "updated_at": created_at,
        "phases": {
            phase: {
                "status": "in_progress" if phase == "planificacion" else "pending",
                "updated_at": created_at,
                "note": "",
            }
            for phase in PHASES
        },
    }
    write_json(root / PROJECT_PATHS["state"], state)
    ensure_csv(root / PROJECT_PATHS["log"], BITACORA_FIELDS)
    ensure_csv(root / PROJECT_PATHS["inventory"], INVENTORY_FIELDS)
    append_log(root, "planificacion", "in_progress", "Proyecto Kitchenham inicializado")
    print(
        json.dumps(
            {
                "project_dir": str(root),
                "status": "initialized",
                "expected_thresholds": expected,
                "source_strategy": source_strategy,
                "search_update": search_update,
                "fulltext_policy": dict(DEFAULT_FULLTEXT_POLICY),
            },
            ensure_ascii=False,
        )
    )
    return 0


def unique_destination(directory: Path, original_name: str, code: str) -> Path:
    base = directory / f"{code}_{now_stamp()}_{safe_name(original_name)}"
    if not base.exists():
        return base
    counter = 2
    while True:
        candidate = directory / f"{base.stem}_{counter}{base.suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def numbered_child_directory(parent: Path, label: str) -> Path:
    parent.mkdir(parents=True, exist_ok=True)
    safe_label = safe_name(label).casefold()
    existing_numbers: list[int] = []
    for child in parent.iterdir():
        if not child.is_dir():
            continue
        match = re.match(r"^(\d{2})_(.+)$", child.name)
        if not match:
            continue
        existing_numbers.append(int(match.group(1)))
        if match.group(2).casefold() == safe_label:
            return child
    next_number = max(existing_numbers, default=0) + 1
    return parent / f"{next_number:02d}_{safe_label}"


def sync_fulltext_metadata(root: Path, inventory_row: dict[str, Any]) -> None:
    source_id = str(inventory_row.get("source_id", "")).strip()
    study_id = str(inventory_row.get("study_id", "")).strip()
    decision = normalized(inventory_row.get("decision"))
    usage_status = {
        "included": "used",
        "excluded": "excluded",
        "pending": "pending",
        "not-applicable": "pending",
    }.get(decision, decision)
    upsert_csv(
        root / PROJECT_PATHS["used_sources"],
        USED_SOURCE_FIELDS,
        "source_id",
        {
            "source_id": source_id,
            "study_id": study_id,
            "reference_key": source_id,
            "source_role": inventory_row.get("source_role", ""),
            "title": inventory_row.get("title", ""),
            "doi": inventory_row.get("doi", ""),
            "url": inventory_row.get("url", ""),
            "inventory_record_id": inventory_row.get("record_id", ""),
            "stored_path": inventory_row.get("stored_path", ""),
            "sha256": inventory_row.get("sha256", ""),
            "download_status": inventory_row.get("download_status", ""),
            "content_reviewed": inventory_row.get("content_reviewed", ""),
            "citations_reviewed": inventory_row.get("citations_reviewed", ""),
            "reviewed_by": inventory_row.get("reviewed_by", ""),
            "reviewed_at": inventory_row.get("reviewed_at", ""),
            "usage_status": usage_status,
            "exclusion_reason": inventory_row.get("exclusion_reason", ""),
            "notes": "",
        },
    )

    if not study_id:
        return
    master_path = root / PROJECT_PATHS["master_records"]
    ensure_csv(master_path, MASTER_FIELDS)
    master_rows = read_csv(master_path)
    changed = False
    for row in master_rows:
        if row.get("study_id", "").strip() != study_id:
            continue
        if decision == "included":
            row.update(
                {
                    "fulltext_record_id": inventory_row.get("record_id", ""),
                    "fulltext_path": inventory_row.get("stored_path", ""),
                    "fulltext_sha256": inventory_row.get("sha256", ""),
                    "download_status": inventory_row.get("download_status", ""),
                    "content_reviewed": inventory_row.get("content_reviewed", ""),
                    "citations_reviewed": inventory_row.get(
                        "citations_reviewed", ""
                    ),
                    "reviewed_by": inventory_row.get("reviewed_by", ""),
                    "reviewed_at": inventory_row.get("reviewed_at", ""),
                }
            )
        elif row.get("fulltext_record_id", "").strip() == str(
            inventory_row.get("record_id", "")
        ).strip():
            for field in [
                "fulltext_record_id",
                "fulltext_path",
                "fulltext_sha256",
                "download_status",
                "content_reviewed",
                "citations_reviewed",
                "reviewed_by",
                "reviewed_at",
            ]:
                row[field] = ""
        changed = True
    if changed:
        write_csv(master_path, MASTER_FIELDS, master_rows)


def register_source(args: argparse.Namespace) -> int:
    root = require_project(Path(args.project_dir))
    source = Path(args.file).resolve()
    if not source.is_file():
        raise SystemExit(f"No existe el archivo: {source}")

    study_id = args.study_id.strip()
    source_id = args.source_id.strip() or study_id
    reviewed_at = args.reviewed_at.strip()
    if args.kind == "fulltext":
        if not source_id:
            raise SystemExit(
                "Todo texto completo requiere --source-id o --study-id."
            )
        if args.source_role == "primary-study" and not study_id:
            raise SystemExit(
                "Un texto primario requiere --study-id para vincularlo al corpus."
            )
        if args.decision == "included" and not (
            args.content_reviewed
            and args.citations_reviewed
            and args.reviewed_by.strip()
        ):
            raise SystemExit(
                "Una fuente incluida requiere --content-reviewed, "
                "--citations-reviewed y --reviewed-by."
            )
        if args.decision == "excluded" and not args.exclusion_reason.strip():
            raise SystemExit(
                "Una fuente excluida requiere --exclusion-reason."
            )
        if (
            args.content_reviewed
            or args.citations_reviewed
            or args.reviewed_by.strip()
        ) and not reviewed_at:
            reviewed_at = now_iso()

    if args.kind == "search-export":
        destination_dir = numbered_child_directory(
            root / "02_busquedas/04_resultados/01_brutos",
            args.database or "fuente-desconocida",
        )
        file_code = "02-04-01"
        decision = "not-applicable"
    elif args.kind == "fulltext":
        decision = args.decision
        decision_dir = {
            "included": "01_incluidos",
            "excluded": "02_excluidos",
            "pending": "03_pendientes",
            "not-applicable": "03_pendientes",
        }[decision]
        destination_dir = root / "04_fuentes/01_originales" / decision_dir
        file_code = {
            "included": "04-01-01",
            "excluded": "04-01-02",
            "pending": "04-01-03",
            "not-applicable": "04-01-03",
        }[decision]
    elif args.kind == "supplement":
        decision = args.decision
        decision_dir = {
            "included": "01_incluidos",
            "excluded": "02_excluidos",
            "pending": "03_pendientes",
            "not-applicable": "03_pendientes",
        }[decision]
        destination_dir = root / "04_fuentes/02_suplementos" / decision_dir
        file_code = {
            "included": "04-02-01",
            "excluded": "04-02-02",
            "pending": "04-02-03",
            "not-applicable": "04-02-03",
        }[decision]
    elif args.kind == "metadata":
        destination_dir = root / "04_fuentes/04_metadatos"
        file_code = "04-04"
        decision = args.decision
    else:
        destination_dir = root / "10_respaldo/05_otros"
        file_code = "10-05"
        decision = args.decision

    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = unique_destination(destination_dir, source.name, file_code)
    copy_source(source, destination)
    digest = sha256_file(destination)
    inventory_path = root / PROJECT_PATHS["inventory"]
    ensure_csv(inventory_path, INVENTORY_FIELDS)
    inventory_rows = read_csv(inventory_path)
    record_id = (
        f"SRC-{now_stamp()}-{len(inventory_rows) + 1:06d}-{digest[:8]}"
    )
    relative = destination.relative_to(root).as_posix()
    inventory_row = {
        "record_id": record_id,
        "registered_at": now_iso(),
        "kind": args.kind,
        "decision": decision,
        "source_id": source_id,
        "study_id": study_id,
        "source_role": args.source_role if args.kind == "fulltext" else "",
        "database": args.database,
        "query_id": args.query_id,
        "origin": args.origin,
        "title": args.title,
        "doi": args.doi,
        "url": args.url,
        "original_name": source.name,
        "source_path": str(source),
        "stored_path": relative,
        "size_bytes": destination.stat().st_size,
        "sha256": digest,
        "download_status": (
            "downloaded" if args.kind == "fulltext" else "not-applicable"
        ),
        "content_reviewed": (
            "true" if args.content_reviewed else "false"
        ) if args.kind == "fulltext" else "not-applicable",
        "citations_reviewed": (
            "true" if args.citations_reviewed else "false"
        ) if args.kind == "fulltext" else "not-applicable",
        "reviewed_by": args.reviewed_by,
        "reviewed_at": reviewed_at,
        "exclusion_reason": args.exclusion_reason,
    }
    append_csv(
        inventory_path,
        INVENTORY_FIELDS,
        inventory_row,
    )
    if args.kind == "fulltext":
        sync_fulltext_metadata(root, inventory_row)
    append_log(
        root,
        "busqueda" if args.kind == "search-export" else "fuentes",
        "in_progress",
        f"Fuente registrada: {record_id}",
        relative,
    )
    print(
        json.dumps(
            {
                "record_id": record_id,
                "stored_path": str(destination),
                "sha256": digest,
            },
            ensure_ascii=False,
        )
    )
    return 0


def review_source(args: argparse.Namespace) -> int:
    root = require_project(Path(args.project_dir))
    inventory_path = root / PROJECT_PATHS["inventory"]
    ensure_csv(inventory_path, INVENTORY_FIELDS)
    rows = read_csv(inventory_path)
    matches = [
        row
        for row in rows
        if row.get("record_id", "").strip() == args.record_id.strip()
    ]
    if len(matches) != 1:
        raise SystemExit(
            "El record_id debe identificar exactamente un archivo inventariado."
        )
    row = matches[0]
    if normalized(row.get("kind")) != "fulltext":
        raise SystemExit("Solo se puede revisar una fuente de tipo fulltext.")
    if args.decision == "included" and not (
        args.content_reviewed
        and args.citations_reviewed
        and args.reviewed_by.strip()
    ):
        raise SystemExit(
            "Una fuente incluida requiere --content-reviewed, "
            "--citations-reviewed y --reviewed-by."
        )
    if args.decision == "excluded" and not args.exclusion_reason.strip():
        raise SystemExit("Una fuente excluida requiere --exclusion-reason.")

    stored = (root / row.get("stored_path", "")).resolve()
    if not stored.is_relative_to(root.resolve()):
        raise SystemExit("La ruta inventariada queda fuera del proyecto.")
    if not stored.is_file():
        raise SystemExit(f"No existe el archivo inventariado: {stored}")
    digest = sha256_file(stored)
    if digest != row.get("sha256", ""):
        raise SystemExit("El hash del texto completo cambió; ejecutar auditoría.")

    decision_dir = {
        "included": "01_incluidos",
        "excluded": "02_excluidos",
    }[args.decision]
    file_code = {
        "included": "04-01-01",
        "excluded": "04-01-02",
    }[args.decision]
    destination_dir = root / "04_fuentes/01_originales" / decision_dir
    destination_dir.mkdir(parents=True, exist_ok=True)
    if stored.parent.resolve() != destination_dir.resolve():
        destination = unique_destination(
            destination_dir,
            row.get("original_name", stored.name),
            file_code,
        )
        copy_source(stored, destination)
        if sha256_file(destination) != digest:
            raise SystemExit('La copia no coincide; se conserva el archivo original.')
        stored.unlink()
    else:
        destination = stored
    if sha256_file(destination) != digest:
        raise SystemExit("El archivo cambió durante su clasificación.")

    row.update(
        {
            "decision": args.decision,
            "stored_path": destination.relative_to(root).as_posix(),
            "size_bytes": destination.stat().st_size,
            "download_status": "downloaded",
            "content_reviewed": (
                "true" if args.content_reviewed else "false"
            ),
            "citations_reviewed": (
                "true" if args.citations_reviewed else "false"
            ),
            "reviewed_by": args.reviewed_by,
            "reviewed_at": args.reviewed_at.strip() or now_iso(),
            "exclusion_reason": args.exclusion_reason,
        }
    )
    write_csv(inventory_path, INVENTORY_FIELDS, rows)
    sync_fulltext_metadata(root, row)
    append_log(
        root,
        "fuentes",
        "completed" if args.decision == "included" else "in_progress",
        f"Revisión manual de fuente: {args.record_id}",
        row["stored_path"],
        actor=args.reviewed_by,
    )
    print(
        json.dumps(
            {
                "record_id": args.record_id,
                "decision": args.decision,
                "stored_path": str(destination),
                "sha256": digest,
                "content_reviewed": args.content_reviewed,
                "citations_reviewed": args.citations_reviewed,
                "reviewed_by": args.reviewed_by,
                "reviewed_at": row["reviewed_at"],
            },
            ensure_ascii=False,
        )
    )
    return 0


def project_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if relative.parts[:2] == ("10_respaldo", "02_snapshots"):
            continue
        files.append(path)
    return sorted(files, key=lambda item: item.relative_to(root).as_posix())


def create_snapshot(root: Path, phase: str, note: str = "") -> dict[str, str]:
    root = require_project(root)
    stamp = now_stamp()
    manifest_path = unique_destination(
        root / "10_respaldo/01_manifiestos",
        f"manifest-{phase}-{stamp}.csv",
        "10-01",
    )
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with io.StringIO(newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=["path", "size_bytes", "sha256", "modified_at"],
        )
        writer.writeheader()
        for path in project_files(root):
            stat = path.stat()
            writer.writerow(
                {
                    "path": path.relative_to(root).as_posix(),
                    "size_bytes": stat.st_size,
                    "sha256": sha256_file(path),
                    "modified_at": datetime.fromtimestamp(
                        stat.st_mtime
                    ).astimezone().isoformat(timespec="seconds"),
                }
            )

        atomic_write(manifest_path, stream.getvalue())

    snapshot_path = unique_destination(
        root / "10_respaldo/02_snapshots",
        f"kitchenham-{phase}-{stamp}.zip",
        "10-02",
    )
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output(snapshot_path) as output, zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in project_files(root):
            archive.write(path, path.relative_to(root).as_posix())
    append_log(root, phase, "completed", "Snapshot creado", note or snapshot_path.name)
    return {
        "snapshot": str(snapshot_path),
        "manifest": str(manifest_path),
        "sha256": sha256_file(snapshot_path),
    }


def snapshot_command(args: argparse.Namespace) -> int:
    print(
        json.dumps(
            create_snapshot(Path(args.project_dir), args.phase, args.note),
            ensure_ascii=False,
        )
    )
    return 0


def source_memberships(row: dict[str, str]) -> list[str]:
    return split_multi(row.get("source_database"))


def marginal_contribution_rows(
    search_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
    master_rows: list[dict[str, str]],
    included_ids: set[str],
) -> list[dict[str, Any]]:
    sources: dict[str, tuple[str, str]] = {}
    for row in source_rows:
        source_id = row.get("source_id", "").strip()
        source_name = row.get("source_name", "").strip()
        key = normalized(source_id or source_name)
        if key:
            sources[key] = (source_id or source_name, source_name or source_id)
    for row in search_rows:
        source_id = row.get("source_id", "").strip()
        source_name = row.get("database", "").strip()
        key = normalized(source_id or source_name)
        if key and key not in sources:
            sources[key] = (source_id or source_name, source_name or source_id)

    output: list[dict[str, Any]] = []
    for key, (source_id, source_name) in sorted(
        sources.items(),
        key=lambda item: item[1][1].casefold(),
    ):
        def belongs(row: dict[str, str]) -> bool:
            memberships = [normalized(item) for item in source_memberships(row)]
            return key in memberships or normalized(source_name) in memberships

        raw_records = sum(
            int(number(row.get("results_count"), 0))
            for row in search_rows
            if normalized(row.get("source_id") or row.get("database")) == key
            or normalized(row.get("database")) == normalized(source_name)
        )
        source_master = [row for row in master_rows if belongs(row)]
        duplicates = sum(bool(row.get("duplicate_of", "").strip()) for row in source_master)
        unique_new = sum(
            not row.get("duplicate_of", "").strip()
            and len(source_memberships(row)) == 1
            for row in source_master
        )
        source_included = [
            row
            for row in source_master
            if row.get("study_id", "").strip() in included_ids
        ]
        exclusive_included = sum(
            len(source_memberships(row)) == 1 for row in source_included
        )
        percentage = (
            exclusive_included / len(included_ids) * 100 if included_ids else 0.0
        )
        output.append(
            {
                "source_id": source_id,
                "source_name": source_name,
                "raw_records": raw_records,
                "duplicate_records": duplicates,
                "unique_new_records": unique_new,
                "screened_records": len(source_master),
                "included_records": len(source_included),
                "exclusive_included_records": exclusive_included,
                "exclusive_included_percentage": f"{percentage:.2f}",
                "calculated_at": now_iso(),
                "notes": (
                    "Los registros únicos nuevos se aproximan mediante registros "
                    "no duplicados asociados exclusivamente a esta fuente."
                ),
            }
        )
    return output


def saturation_statuses(root: Path) -> dict[str, str]:
    rows = read_csv(root / PROJECT_PATHS["saturation"])
    return {
        normalized(row.get("criterion")): normalized(row.get("status"))
        for row in rows
        if row.get("criterion", "").strip()
    }


def status_positive(value: str) -> bool:
    return value in {"pass", "passed", "complete", "completed", "yes", "si", "sí", "na"}


def coverage_metrics(root: Path, config: dict[str, Any] | None = None) -> dict[str, Any]:
    config = effective_config(config or read_json(root / PROJECT_PATHS["config"]))
    expected = config["expected_thresholds"]
    source_strategy = config["source_strategy"]
    search_update = config["search_update"]

    search_rows = read_csv(root / PROJECT_PATHS["search_registry"])
    source_rows_all = read_csv(root / PROJECT_PATHS["consulted_sources"])
    source_rows = [row for row in source_rows_all if is_true(row.get("search_executed"))]
    source_names = sorted(
        {
            row.get("source_name", "").strip()
            for row in source_rows
            if row.get("source_name", "").strip()
        },
        key=str.casefold,
    )

    search_dates = [
        parsed
        for parsed in (parse_iso_date(row.get("search_date")) for row in search_rows)
        if parsed
    ]
    latest_search = max(search_dates) if search_dates else None
    search_age_days = (date.today() - latest_search).days if latest_search else None
    required_search_fields = [
        "search_id",
        "database",
        "search_date",
        "query_file",
        "results_count",
        "export_file",
    ]
    search_traceability_gaps = [
        row.get("search_id", "(sin ID)")
        for row in search_rows
        if any(not str(row.get(field, "")).strip() for field in required_search_fields)
    ]

    master_rows = read_csv(root / PROJECT_PATHS["master_records"])
    deduplicated_rows = [
        row
        for row in master_rows
        if not row.get("duplicate_of", "").strip()
        and normalized(row.get("status")) not in {"duplicate", "duplicado"}
    ]
    candidate_ids = {
        row.get("study_id", "").strip()
        for row in deduplicated_rows
        if row.get("study_id", "").strip()
    }
    candidate_count = len(candidate_ids) if candidate_ids else len(deduplicated_rows)

    included_labels = {"included", "incluido", "include", "incluir"}
    excluded_labels = {"excluded", "excluido", "exclude", "excluir"}
    included_ids = {
        row.get("study_id", "").strip()
        for row in deduplicated_rows
        if row.get("study_id", "").strip()
        and normalized(row.get("status")) in included_labels
    }
    screening_rows = read_csv(root / PROJECT_PATHS["screening"])
    fulltext_ids: set[str] = set()
    for row in screening_rows:
        stage = normalized(row.get("stage"))
        decision = normalized(row.get("decision"))
        study_id = row.get("study_id", "").strip()
        if study_id and ("full" in stage or "completo" in stage):
            if decision in included_labels | excluded_labels:
                fulltext_ids.add(study_id)
            if decision in included_labels:
                included_ids.add(study_id)
    fulltext_ids.update(
        row.get("study_id", "").strip()
        for row in read_csv(root / PROJECT_PATHS["fulltext_exclusions"])
        if row.get("study_id", "").strip()
    )
    fulltext_ids.update(included_ids)

    years_by_id: dict[str, int] = {}
    for row in deduplicated_rows:
        study_id = row.get("study_id", "").strip()
        try:
            year = int(row.get("year", "").strip())
        except (ValueError, AttributeError):
            continue
        if study_id:
            years_by_id[study_id] = year
    recent_start = date.today().year - int(expected["recent_window_years"]) + 1
    included_years = [years_by_id[item] for item in included_ids if item in years_by_id]
    recent_count = sum(year >= recent_start for year in included_years)
    recent_percentage = recent_count / len(included_ids) * 100 if included_ids else 0.0
    year_distribution: dict[int, int] = {}
    for year in included_years:
        year_distribution[year] = year_distribution.get(year, 0) + 1

    roles = {normalized(row.get("role")) for row in source_rows}
    source_types = {normalized(row.get("source_type")) for row in source_rows}
    source_groups = {
        normalized(row.get("independence_group") or row.get("source_name"))
        for row in source_rows
        if row.get("source_name", "").strip()
    }
    role_groups: dict[str, set[str]] = {}
    for row in source_rows:
        role = normalized(row.get("role"))
        group = normalized(row.get("independence_group") or row.get("source_name"))
        if role and group:
            role_groups.setdefault(role, set()).add(group)
    main_groups = (
        role_groups.get("multidisciplinary", set())
        | role_groups.get("domain_specialized", set())
    )
    complement_groups = role_groups.get("independent_complement", set())
    independent_complement = bool(complement_groups - main_groups)

    disciplines = [normalized(item) for item in config.get("disciplines", []) if item]
    uncovered_disciplines = [
        discipline
        for discipline in disciplines
        if not any(
            discipline in normalized(row.get("discipline_coverage"))
            for row in source_rows
        )
    ]

    planned = [item for item in config.get("planned_databases", []) if item]
    executed_names = {normalized(name) for name in source_names}
    unconsulted_rows = read_csv(root / PROJECT_PATHS["unconsulted_sources"])
    documented_unconsulted = {
        normalized(row.get("source_name"))
        for row in unconsulted_rows
        if row.get("source_name", "").strip()
        and row.get("access_or_exclusion_reason", "").strip()
        and row.get("coverage_impact", "").strip()
    }
    undocumented_planned_sources = [
        name
        for name in planned
        if normalized(name) not in executed_names
        and normalized(name) not in documented_unconsulted
    ]
    complement_absence_justified = any(
        row.get("access_or_exclusion_reason", "").strip()
        and row.get("coverage_impact", "").strip()
        and row.get("mitigation", "").strip()
        for row in unconsulted_rows
    )

    seed_rows = [
        row
        for row in read_csv(root / PROJECT_PATHS["seed_articles"])
        if row.get("seed_id", "").strip() or row.get("title", "").strip()
    ]
    available_seeds = [row for row in seed_rows if is_true(row.get("available"))]
    recovered_seeds = [row for row in available_seeds if is_true(row.get("recovered"))]
    seed_recovery_percentage = (
        len(recovered_seeds) / len(available_seeds) * 100
        if available_seeds
        else None
    )

    saturation = saturation_statuses(root)
    snowball_rows = read_csv(root / PROJECT_PATHS["snowballing"])
    backward_done = any(
        normalized(row.get("direction")) in {"backward", "retrospective", "retrospectivo"}
        for row in snowball_rows
    ) or status_positive(saturation.get("backward_snowballing_complete", ""))
    forward_done = any(
        normalized(row.get("direction")) in {"forward", "prospective", "prospectivo"}
        for row in snowball_rows
    ) or status_positive(saturation.get("forward_snowballing_complete", ""))
    rounds = [row.get("round", "").strip() for row in snowball_rows if row.get("round")]
    last_round = rounds[-1] if rounds else None
    if rounds and all(item.isdigit() for item in rounds):
        last_round = str(max(int(item) for item in rounds))
    last_round_rows = [
        row for row in snowball_rows if row.get("round", "").strip() == last_round
    ]
    last_round_included = sum(
        normalized(row.get("decision")) in included_labels for row in last_round_rows
    )
    snowball_saturated = (
        bool(last_round_rows) and last_round_included == 0
    ) or status_positive(saturation.get("snowballing_zero_new_round", ""))

    inventory_rows = read_csv(root / PROJECT_PATHS["inventory"])
    inventory_by_record = {
        row.get("record_id", "").strip(): row
        for row in inventory_rows
        if row.get("record_id", "").strip()
    }
    search_exports = [
        row for row in inventory_rows if normalized(row.get("kind")) == "search-export"
    ]
    export_sources = {
        normalized(row.get("database"))
        for row in search_exports
        if row.get("database", "").strip()
    }
    unregistered_export_sources = [
        name for name in source_names if normalized(name) not in export_sources
    ]
    fulltexts_registered = len(
        {
            row.get("record_id", "").strip()
            for row in inventory_rows
            if normalized(row.get("kind")) == "fulltext"
            and row.get("record_id", "").strip()
        }
    )
    reviewed_fulltext_records: set[str] = set()
    reviewed_fulltext_study_ids: set[str] = set()
    for row in inventory_rows:
        record_id = row.get("record_id", "").strip()
        stored_path = row.get("stored_path", "").strip().replace("\\", "/")
        if (
            normalized(row.get("kind")) == "fulltext"
            and normalized(row.get("decision")) == "included"
            and normalized(row.get("download_status")) == "downloaded"
            and is_true(row.get("content_reviewed"))
            and is_true(row.get("citations_reviewed"))
            and row.get("reviewed_by", "").strip()
            and row.get("reviewed_at", "").strip()
            and stored_path.startswith(
                "04_fuentes/01_originales/01_incluidos/"
            )
        ):
            reviewed_fulltext_records.add(record_id)
            study_id = row.get("study_id", "").strip()
            if study_id:
                reviewed_fulltext_study_ids.add(study_id)

    master_by_id = {
        row.get("study_id", "").strip(): row
        for row in deduplicated_rows
        if row.get("study_id", "").strip()
    }
    included_download_issues: list[str] = []
    for study_id in sorted(included_ids, key=str.casefold):
        master_row = master_by_id.get(study_id)
        if not master_row:
            included_download_issues.append(
                f"{study_id}: no existe vínculo en el registro maestro"
            )
            continue
        record_id = master_row.get("fulltext_record_id", "").strip()
        if not record_id:
            included_download_issues.append(
                f"{study_id}: falta fulltext_record_id"
            )
            continue
        inventory_row = inventory_by_record.get(record_id)
        if not inventory_row:
            included_download_issues.append(
                f"{study_id}: fulltext_record_id no existe en el inventario"
            )
            continue
        if inventory_row.get("study_id", "").strip() != study_id:
            included_download_issues.append(
                f"{study_id}: el texto inventariado pertenece a otro study_id"
            )
            continue
        if record_id not in reviewed_fulltext_records:
            included_download_issues.append(
                f"{study_id}: texto no descargado, no incluido o sin revisión "
                "manual completa de contenido y citas"
            )
            continue
        expected_values = {
            "fulltext_path": inventory_row.get("stored_path", "").strip(),
            "fulltext_sha256": inventory_row.get("sha256", "").strip(),
            "download_status": "downloaded",
        }
        mismatches = [
            field
            for field, value in expected_values.items()
            if normalized(master_row.get(field)) != normalized(value)
        ]
        if not is_true(master_row.get("content_reviewed")):
            mismatches.append("content_reviewed")
        if not is_true(master_row.get("citations_reviewed")):
            mismatches.append("citations_reviewed")
        if not master_row.get("reviewed_by", "").strip():
            mismatches.append("reviewed_by")
        if not master_row.get("reviewed_at", "").strip():
            mismatches.append("reviewed_at")
        if mismatches:
            included_download_issues.append(
                f"{study_id}: vínculo maestro incompleto ({', '.join(mismatches)})"
            )

    used_source_rows = [
        row
        for row in read_csv(root / PROJECT_PATHS["used_sources"])
        if normalized(row.get("usage_status")) in {"used", "cited", "included"}
    ]
    used_source_issues: list[str] = []
    reviewed_used_source_ids: set[str] = set()
    for row in used_source_rows:
        source_id = row.get("source_id", "").strip()
        label = source_id or "(sin source_id)"
        record_id = row.get("inventory_record_id", "").strip()
        inventory_row = inventory_by_record.get(record_id)
        if not source_id:
            used_source_issues.append(f"{label}: falta source_id")
            continue
        if not inventory_row:
            used_source_issues.append(
                f"{label}: no existe inventory_record_id válido"
            )
            continue
        checks_ok = (
            normalized(inventory_row.get("kind")) == "fulltext"
            and record_id in reviewed_fulltext_records
            and normalized(row.get("download_status")) == "downloaded"
            and is_true(row.get("content_reviewed"))
            and is_true(row.get("citations_reviewed"))
            and row.get("reviewed_by", "").strip()
            and row.get("reviewed_at", "").strip()
            and row.get("stored_path", "").strip()
            == inventory_row.get("stored_path", "").strip()
            and row.get("sha256", "").strip()
            == inventory_row.get("sha256", "").strip()
        )
        if checks_ok:
            reviewed_used_source_ids.add(source_id)
        else:
            used_source_issues.append(
                f"{label}: descarga, vínculo, hash o revisión manual incompletos"
            )

    used_study_ids = {
        row.get("study_id", "").strip()
        for row in used_source_rows
        if row.get("study_id", "").strip()
        and row.get("source_id", "").strip() in reviewed_used_source_ids
    }
    for study_id in sorted(included_ids - used_study_ids, key=str.casefold):
        included_download_issues.append(
            f"{study_id}: no figura como fuente usada y revisada"
        )

    evidence_study_ids = {
        row.get("study_id", "").strip()
        for path_key in ["quality", "extraction"]
        for row in read_csv(root / PROJECT_PATHS[path_key])
        if row.get("study_id", "").strip()
    }
    for row in read_csv(root / PROJECT_PATHS["evidence_map"]):
        evidence_study_ids.update(split_multi(row.get("study_ids")))
    unreviewed_evidence_study_ids = sorted(
        evidence_study_ids - reviewed_fulltext_study_ids,
        key=str.casefold,
    )

    citation_rows = [
        row
        for row in read_csv(root / PROJECT_PATHS["citation_audit"])
        if row.get("citation_id", "").strip() or row.get("source_id", "").strip()
    ]
    verified_citation_source_ids = {
        row.get("source_id", "").strip()
        for row in citation_rows
        if row.get("source_id", "").strip()
        and is_true(row.get("verified_against_local_file"))
        and is_true(row.get("content_consistent"))
        and is_true(row.get("citation_consistent"))
        and row.get("local_locator", "").strip()
        and row.get("reviewer", "").strip()
        and row.get("reviewed_at", "").strip()
        and normalized(row.get("status")) in {
            "verified",
            "completed",
            "complete",
            "ok",
            "pass",
        }
    }
    citation_unknown_source_ids = sorted(
        {
            row.get("source_id", "").strip()
            for row in citation_rows
            if row.get("source_id", "").strip()
        }
        - {row.get("source_id", "").strip() for row in used_source_rows},
        key=str.casefold,
    )
    impact_ids = {
        row.get("study_id", "").strip()
        for row in read_csv(root / PROJECT_PATHS["impact"])
        if row.get("study_id", "").strip()
    }
    gap_rows = read_csv(root / PROJECT_PATHS["gaps"])
    marginal_rows = marginal_contribution_rows(
        search_rows,
        source_rows,
        master_rows,
        included_ids,
    )
    return {
        "expected_thresholds": expected,
        "source_strategy": source_strategy,
        "search_update": search_update,
        "fulltext_policy": config["fulltext_policy"],
        "search_audit": config["search_audit"],
        "disciplines": config.get("disciplines", []),
        "executed_sources": len(source_rows),
        "source_names": source_names,
        "source_types": sorted(item for item in source_types if item),
        "independence_groups": len(source_groups),
        "has_multidisciplinary_source": "multidisciplinary" in roles,
        "has_domain_specialized_source": "domain_specialized" in roles,
        "has_independent_complement": independent_complement,
        "complement_absence_justified": complement_absence_justified,
        "source_justifications_missing": [
            row.get("source_name", "")
            for row in source_rows
            if not row.get("selection_justification", "").strip()
        ],
        "invalid_source_types": [
            row.get("source_name", "")
            for row in source_rows
            if normalized(row.get("source_type")) not in SOURCE_TYPES
        ],
        "invalid_source_roles": [
            row.get("source_name", "")
            for row in source_rows
            if normalized(row.get("role")) not in SOURCE_ROLES
        ],
        "uncovered_disciplines": uncovered_disciplines,
        "undocumented_planned_sources": undocumented_planned_sources,
        "unconsulted_sources_documented": len(unconsulted_rows),
        "search_queries": len(search_rows),
        "search_traceability_gaps": search_traceability_gaps,
        "registered_search_exports": len(search_exports),
        "unregistered_export_sources": unregistered_export_sources,
        "seed_articles_defined": len(seed_rows),
        "seed_articles_available": len(available_seeds),
        "seed_articles_recovered": len(recovered_seeds),
        "seed_recovery_percentage": (
            round(seed_recovery_percentage, 2)
            if seed_recovery_percentage is not None
            else None
        ),
        "backward_snowballing_done": backward_done,
        "forward_snowballing_done": forward_done,
        "snowballing_last_round": last_round,
        "snowballing_last_round_included": last_round_included,
        "snowballing_saturated": snowball_saturated,
        "terminology_variants_covered": status_positive(
            saturation.get("terminology_variants_covered", "")
        ),
        "no_obvious_disciplinary_gaps": status_positive(
            saturation.get("no_obvious_disciplinary_gaps", "")
        ),
        "marginal_yield_stabilized": status_positive(
            saturation.get("marginal_yield_stabilized", "")
        ),
        "candidates_after_dedup": candidate_count,
        "fulltexts_assessed": len(fulltext_ids),
        "fulltexts_registered": fulltexts_registered,
        "included_studies": len(included_ids),
        "reviewed_fulltexts": len(reviewed_fulltext_records),
        "reviewed_used_sources": len(reviewed_used_source_ids),
        "included_download_issues": included_download_issues,
        "used_source_issues": used_source_issues,
        "unreviewed_evidence_study_ids": unreviewed_evidence_study_ids,
        "used_source_ids": sorted(
            {
                row.get("source_id", "").strip()
                for row in used_source_rows
                if row.get("source_id", "").strip()
            },
            key=str.casefold,
        ),
        "verified_citation_source_ids": sorted(
            verified_citation_source_ids,
            key=str.casefold,
        ),
        "citation_unknown_source_ids": citation_unknown_source_ids,
        "recent_window_start": recent_start,
        "recent_studies": recent_count,
        "recent_evidence_percentage": round(recent_percentage, 2),
        "included_without_valid_year": len(included_ids) - len(included_years),
        "year_distribution": {
            str(year): count for year, count in sorted(year_distribution.items())
        },
        "impact_studies_evaluated": len(impact_ids),
        "novelty_gaps_documented": len(gap_rows),
        "latest_search_date": latest_search.isoformat() if latest_search else None,
        "final_search_age_days": search_age_days,
        "marginal_contribution": marginal_rows,
    }


def expected_shortfalls(metrics: dict[str, Any]) -> list[dict[str, Any]]:
    expected = metrics["expected_thresholds"]
    checks = [
        (
            "unique_records",
            metrics["candidates_after_dedup"],
            number(expected["unique_records"]),
        ),
        (
            "full_texts_assessed",
            metrics["fulltexts_assessed"],
            number(expected["full_texts_assessed"]),
        ),
        (
            "included_studies",
            metrics["included_studies"],
            number(expected["included_studies"]),
        ),
        (
            "recent_evidence_percentage",
            metrics["recent_evidence_percentage"],
            number(expected["recent_evidence_percentage"]),
        ),
    ]
    return [
        {"threshold": key, "obtained": actual, "expected": target}
        for key, actual, target in checks
        if actual < target
    ]


def methodological_coverage_issues(metrics: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if metrics["search_queries"] == 0:
        issues.append("No existen búsquedas ejecutadas y registradas.")
    if metrics["executed_sources"] == 0:
        issues.append("No existe una tabla de fuentes ejecutadas y clasificadas.")
    if not metrics["disciplines"]:
        issues.append("No se documentaron las disciplinas implicadas.")
    if not metrics["has_multidisciplinary_source"]:
        issues.append("Falta una fuente multidisciplinaria.")
    if not metrics["has_domain_specialized_source"]:
        issues.append("Falta una fuente especializada en el dominio.")
    if (
        not metrics["has_independent_complement"]
        and not metrics["complement_absence_justified"]
    ):
        issues.append(
            "Falta una fuente independiente complementaria o una justificación "
            "documentada de su ausencia."
        )
    if not metrics["backward_snowballing_done"]:
        issues.append("No se documentó búsqueda retrospectiva.")
    if not metrics["forward_snowballing_done"]:
        issues.append("No se documentó búsqueda prospectiva.")
    if metrics["source_justifications_missing"]:
        issues.append(
            "Fuentes sin justificación: "
            + ", ".join(metrics["source_justifications_missing"])
            + "."
        )
    if metrics["invalid_source_types"]:
        issues.append(
            "Fuentes con tipo inválido: "
            + ", ".join(metrics["invalid_source_types"])
            + "."
        )
    if metrics["invalid_source_roles"]:
        issues.append(
            "Fuentes con función inválida: "
            + ", ".join(metrics["invalid_source_roles"])
            + "."
        )
    if metrics["uncovered_disciplines"]:
        issues.append(
            "Disciplinas sin cobertura explícita: "
            + ", ".join(metrics["uncovered_disciplines"])
            + "."
        )
    if metrics["undocumented_planned_sources"]:
        issues.append(
            "Fuentes previstas no ejecutadas ni justificadas: "
            + ", ".join(metrics["undocumented_planned_sources"])
            + "."
        )
    if metrics["search_traceability_gaps"]:
        issues.append(
            "Búsquedas con campos de trazabilidad incompletos: "
            + ", ".join(metrics["search_traceability_gaps"])
            + "."
        )
    if metrics["unregistered_export_sources"]:
        issues.append(
            "Fuentes sin exportación bruta inventariada: "
            + ", ".join(metrics["unregistered_export_sources"])
            + "."
        )
    return issues


def advisory_signals(metrics: dict[str, Any]) -> list[str]:
    signals = [
        f"{item['threshold']}: {item['obtained']}/{item['expected']}"
        for item in expected_shortfalls(metrics)
    ]
    strategy = metrics["source_strategy"]
    if metrics["executed_sources"] < int(strategy["recommended_main_sources_min"]):
        signals.append(
            "Fuentes principales por debajo del rango recomendado: "
            f"{metrics['executed_sources']}/"
            f"{strategy['recommended_main_sources_min']}."
        )
    if (
        not strategy.get("seed_articles_unavailable")
        and metrics["seed_articles_defined"] == 0
    ):
        signals.append(
            "No se definieron artículos semilla ni se justificó su indisponibilidad."
        )
    target = number(strategy["seed_recovery_target_percentage"])
    recovery = metrics["seed_recovery_percentage"]
    if recovery is not None and recovery < target:
        signals.append(f"Recuperación de semillas: {recovery:.1f}%/{target:.1f}%.")
    marginal_limit = number(strategy["marginal_contribution_warning_percentage"])
    for row in metrics["marginal_contribution"]:
        percentage = number(row.get("exclusive_included_percentage"))
        if percentage <= marginal_limit:
            signals.append(
                f"Aporte exclusivo marginal de {row['source_name']}: "
                f"{percentage:.2f}%."
            )
    if not metrics["snowballing_saturated"]:
        signals.append(
            "No se documentó una ronda completa de búsqueda complementaria "
            "sin nuevas inclusiones."
        )
    if not metrics["terminology_variants_covered"]:
        signals.append("La cobertura de variantes terminológicas no está validada.")
    if not metrics["no_obvious_disciplinary_gaps"]:
        signals.append("La ausencia de vacíos disciplinares no está validada.")
    if not metrics["marginal_yield_stabilized"]:
        signals.append("La estabilización del aporte marginal no está validada.")
    age = metrics["final_search_age_days"]
    update = metrics["search_update"]
    if age is None:
        signals.append("No existe fecha válida de la última búsqueda.")
    elif age < 0:
        signals.append("La última fecha de búsqueda está en el futuro.")
    elif age > int(update["recommended_max_age_days"]):
        signals.append(
            f"Antigüedad de búsqueda: {age}/"
            f"{update['recommended_max_age_days']} días recomendados."
        )
    return signals


def external_volume_failures(metrics: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    expected = metrics["expected_thresholds"]
    if expected.get("enforcement") == "external_requirement":
        source = expected.get("external_requirement_source") or "autoridad no indicada"
        failures.extend(
            f"Requisito externo ({source}) incumplido: "
            f"{item['threshold']} {item['obtained']}/{item['expected']}."
            for item in expected_shortfalls(metrics)
        )
    return failures


def external_update_failures(metrics: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    update = metrics["search_update"]
    age = metrics["final_search_age_days"]
    if update.get("enforcement") == "external_requirement":
        if age is None or age < 0 or age > int(update["recommended_max_age_days"]):
            source = update.get("external_requirement_source") or "autoridad no indicada"
            failures.append(
                f"Requisito externo de actualización de búsqueda ({source}) incumplido."
            )
    return failures


def external_requirement_failures(metrics: dict[str, Any]) -> list[str]:
    return external_volume_failures(metrics) + external_update_failures(metrics)


def control_assessment(
    metrics: dict[str, Any],
    severe_errors: list[str] | None = None,
) -> dict[str, Any]:
    severe_errors = severe_errors or []
    coverage_issues = methodological_coverage_issues(metrics)
    signals = advisory_signals(metrics)
    external_failures = external_requirement_failures(metrics)
    audit = metrics["search_audit"]
    decision = normalized(audit.get("decision"))
    if severe_errors:
        status = "BLOCKED"
    elif external_failures or decision in {"modify-period", "amend-scope"}:
        status = "REQUIRES_PROTOCOL_AMENDMENT"
    elif coverage_issues:
        status = "REQUIRES_SEARCH_AUDIT"
    elif signals and not audit.get("completed"):
        status = "REQUIRES_SEARCH_AUDIT"
    elif signals:
        status = "PASS_WITH_WARNINGS"
    else:
        status = "PASS"
    return {
        "status": status,
        "coverage_issues": coverage_issues,
        "advisory_signals": signals,
        "external_requirement_failures": external_failures,
        "severe_errors": severe_errors,
    }


def sync_generated_outputs(root: Path, metrics: dict[str, Any]) -> None:
    write_csv(
        root / PROJECT_PATHS["marginal"],
        MARGINAL_FIELDS,
        metrics["marginal_contribution"],
    )
    total = metrics["included_studies"]
    temporal_rows = [
        {
            "year": year,
            "included_studies": count,
            "percentage": f"{(count / total * 100 if total else 0):.2f}",
        }
        for year, count in metrics["year_distribution"].items()
    ]
    write_csv(
        root / PROJECT_PATHS["temporal"],
        ["year", "included_studies", "percentage"],
        temporal_rows,
    )

    exception_path = root / PROJECT_PATHS["exceptions"]
    audit_completed = bool(metrics["search_audit"].get("completed"))
    active_ids: set[str] = set()
    for item in expected_shortfalls(metrics):
        exception_id = "EXC-AUTO-" + safe_name(item["threshold"]).upper()
        active_ids.add(exception_id)
        upsert_csv(
            exception_path,
            EXCEPTION_FIELDS,
            "exception_id",
            {
                "exception_id": exception_id,
                "date": date.today().isoformat(),
                "responsible": "",
                "threshold": item["threshold"],
                "expected": item["expected"],
                "obtained": item["obtained"],
                "audit_completed": str(audit_completed).lower(),
                "reviews_performed": "",
                "changes_applied": "",
                "justification": "",
                "risk": "",
                "impact": "",
                "decision": "",
                "approved_by": "",
                "status": "draft",
            },
            preserve_finalized=True,
        )
    current_rows = read_csv(exception_path)
    changed = False
    for row in current_rows:
        if (
            row.get("exception_id", "").startswith("EXC-AUTO-")
            and row.get("exception_id") not in active_ids
            and normalized(row.get("status")) == "draft"
        ):
            row["status"] = "resolved-no-longer-needed"
            changed = True
    if changed:
        write_csv(exception_path, EXCEPTION_FIELDS, current_rows)


def phase_gate_issues(root: Path, phase: str) -> list[str]:
    metrics = coverage_metrics(root)
    assessment = control_assessment(metrics)
    issues: list[str] = []
    if phase == "busqueda":
        issues.extend(assessment["coverage_issues"])
    if phase in {"seleccion", "fuentes", "calidad", "extraccion", "sintesis", "informe"}:
        issues.extend(external_volume_failures(metrics))
        issues.extend(
            f"Fuente incluida sin descarga y revisión válidas: {item}"
            for item in metrics["included_download_issues"]
        )
    if phase in {"fuentes", "calidad", "extraccion", "sintesis", "informe"}:
        issues.extend(
            f"Fuente usada sin descarga y revisión válidas: {item}"
            for item in metrics["used_source_issues"]
        )
    if phase in {"calidad", "extraccion", "sintesis", "informe"} and metrics[
        "unreviewed_evidence_study_ids"
    ]:
        issues.append(
            "Se usan estudios sin texto completo local revisado: "
            + ", ".join(metrics["unreviewed_evidence_study_ids"])
            + "."
        )
    if phase in {"sintesis", "informe"}:
        if metrics["impact_studies_evaluated"] < metrics["included_studies"]:
            issues.append(
                "Evaluación de impacto y novedad incompleta: "
                f"{metrics['impact_studies_evaluated']}/"
                f"{metrics['included_studies']} estudios."
            )
        if metrics["novelty_gaps_documented"] == 0:
            issues.append("La matriz de brechas y novedad no contiene hallazgos.")
    if phase == "informe":
        issues.extend(external_update_failures(metrics))
        issues.extend(
            f"Fuente desconocida en auditoría de citas: {source_id}"
            for source_id in metrics["citation_unknown_source_ids"]
        )
        missing_citation_audits = sorted(
            set(metrics["used_source_ids"])
            - set(metrics["verified_citation_source_ids"]),
            key=str.casefold,
        )
        if missing_citation_audits:
            issues.append(
                "Falta verificación manual contra archivo local para: "
                + ", ".join(missing_citation_audits)
                + "."
            )
    return sorted(set(issues))


def update_phase(args: argparse.Namespace) -> int:
    root = require_project(Path(args.project_dir))
    if args.status == "completed":
        issues = phase_gate_issues(root, args.phase)
        if issues:
            raise SystemExit(
                "No se puede cerrar la fase por controles metodológicos o "
                "requisitos externos pendientes:\n- "
                + "\n- ".join(issues)
                + "\nLos valores operativos advisory, por sí solos, no bloquean."
            )
    state_path = root / PROJECT_PATHS["state"]
    state = read_json(state_path)
    updated_at = now_iso()
    state["updated_at"] = updated_at
    state["phases"][args.phase] = {
        "status": args.status,
        "updated_at": updated_at,
        "note": args.note,
    }
    write_json(state_path, state)
    append_log(root, args.phase, args.status, "Estado de fase actualizado", args.note)
    result: dict[str, Any] = {
        "phase": args.phase,
        "status": args.status,
        "updated_at": updated_at,
    }
    if args.status == "completed" and not args.no_snapshot:
        result["backup"] = create_snapshot(root, args.phase, args.note)
    print(json.dumps(result, ensure_ascii=False))
    return 0


def record_search_audit(args: argparse.Namespace) -> int:
    root = require_project(Path(args.project_dir))
    if len(args.review_notes.strip()) < 80:
        raise SystemExit(
            "La auditoría requiere notas de al menos 80 caracteres que cubran "
            "las diez comprobaciones metodológicas."
        )
    config_path = root / PROJECT_PATHS["config"]
    config = read_json(config_path)
    audit = {
        "completed": True,
        "decision": args.decision,
        "reviewed_by": args.reviewed_by.strip(),
        "review_notes": args.review_notes.strip(),
        "updated_at": now_iso(),
    }
    config["search_audit"] = audit
    write_json(config_path, config)
    report = {
        "project": str(root),
        "methodology": "Kitchenham",
        "review_order": [
            "research_questions",
            "synonyms",
            "source_syntax",
            "search_fields",
            "source_pertinence",
            "seed_articles",
            "language_restrictions",
            "time_period",
            "selection_criteria",
            "available_evidence",
        ],
        **audit,
    }
    report_path = (
        root
        / "09_auditorias/03_metodologia"
        / f"09-03_auditoria-busqueda-{now_stamp()}.json"
    )
    write_json(report_path, report)
    append_log(
        root,
        "busqueda",
        "in_progress",
        "Auditoría metodológica de búsqueda registrada",
        args.decision,
    )
    print(
        json.dumps(
            {"search_audit": audit, "report": str(report_path)},
            ensure_ascii=False,
        )
    )
    return 0


def record_methodological_exception(args: argparse.Namespace) -> int:
    root = require_project(Path(args.project_dir))
    for label, value, minimum in [
        ("reviews-performed", args.reviews_performed, 20),
        ("justification", args.justification, 40),
        ("risk", args.risk, 15),
        ("impact", args.impact, 15),
        ("decision", args.decision, 15),
    ]:
        if len(value.strip()) < minimum:
            raise SystemExit(
                f"--{label} requiere al menos {minimum} caracteres concretos."
            )
    config = effective_config(read_json(root / PROJECT_PATHS["config"]))
    payload = {
        "exception_id": args.exception_id,
        "date": date.today().isoformat(),
        "responsible": args.responsible,
        "threshold": args.threshold,
        "expected": args.expected,
        "obtained": args.obtained,
        "audit_completed": str(bool(config["search_audit"].get("completed"))).lower(),
        "reviews_performed": args.reviews_performed,
        "changes_applied": args.changes_applied,
        "justification": args.justification,
        "risk": args.risk,
        "impact": args.impact,
        "decision": args.decision,
        "approved_by": args.approved_by,
        "status": "finalized",
    }
    exception_path = root / PROJECT_PATHS["exceptions"]
    upsert_csv(exception_path, EXCEPTION_FIELDS, "exception_id", payload)
    json_path = (
        root
        / "00_gestion/05_decisiones"
        / f"00-05_{safe_name(args.exception_id)}.json"
    )
    write_json(json_path, payload)
    append_log(
        root,
        "busqueda",
        "in_progress",
        f"Excepción metodológica registrada: {args.exception_id}",
        args.threshold,
    )
    print(
        json.dumps(
            {"exception": payload, "record": str(json_path)},
            ensure_ascii=False,
        )
    )
    return 0


def csv_data_rows(path: Path) -> int:
    return len(read_csv(path))


def layout_violations(root: Path) -> list[str]:
    violations: list[str] = []
    directory_pattern = re.compile(r"^\d{2}_.+")
    file_pattern = re.compile(r"^\d{2}(?:-\d{2})+_.+")
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        directory_parts = relative.parts if path.is_dir() else relative.parts[:-1]
        for part in directory_parts:
            if not directory_pattern.fullmatch(part):
                violations.append(
                    f"Directorio sin numeración de etapa/paso: {relative.as_posix()}"
                )
                break
        if path.is_file() and not file_pattern.fullmatch(path.name):
            violations.append(
                f"Archivo sin prefijo numérico de etapa-paso: {relative.as_posix()}"
            )
    return sorted(set(violations))


def audit_project(args: argparse.Namespace) -> int:
    root = require_project(Path(args.project_dir))
    severe_errors: list[str] = []
    warnings: list[str] = []
    checks: list[dict[str, Any]] = []
    required = list(
        dict.fromkeys(
            [
                PROJECT_PATHS["config"],
                PROJECT_PATHS["state"],
                PROJECT_PATHS["log"],
                PROJECT_PATHS["inventory"],
                *TEMPLATES.values(),
            ]
        )
    )
    for relative in required:
        path = root / relative
        ok = path.exists() and path.stat().st_size > 0
        checks.append({"check": "required_artifact", "path": relative, "ok": ok})
        if not ok:
            severe_errors.append(f"Falta artefacto requerido o está vacío: {relative}")

    raw_config = read_json(root / PROJECT_PATHS["config"])
    config = effective_config(raw_config)
    if not config.get("methodology_exclusive"):
        severe_errors.append(
            "La configuración no declara metodología Kitchenham exclusiva."
        )
    fulltext_policy = config["fulltext_policy"]
    if (
        normalized(fulltext_policy.get("enforcement")) != "mandatory"
        or not is_true(fulltext_policy.get("require_local_fulltext_for_use"))
        or not is_true(fulltext_policy.get("require_content_review"))
        or not is_true(fulltext_policy.get("require_citation_review"))
        or normalized(fulltext_policy.get("inaccessible_decision")) != "excluded"
        or normalized(fulltext_policy.get("exclusion_code"))
        != "ft-no-descargado"
        or is_true(fulltext_policy.get("allow_exception"))
    ):
        severe_errors.append(
            "La política obligatoria de descarga, revisión manual y exclusión "
            "FT-NO-DESCARGADO fue debilitada."
        )

    inventory = root / PROJECT_PATHS["inventory"]
    for row in read_csv(inventory):
        stored = root / row.get("stored_path", "")
        if not stored.is_file():
            severe_errors.append(
                f"Archivo inventariado ausente: {row.get('stored_path')}"
            )
            continue
        if sha256_file(stored) != row.get("sha256"):
            severe_errors.append(f"Hash alterado: {row.get('stored_path')}")

    state = read_json(root / PROJECT_PATHS["state"])
    phase_artifacts = {
        "busqueda": (PROJECT_PATHS["search_registry"], "registro de búsquedas"),
        "seleccion": (PROJECT_PATHS["screening"], "decisiones de cribado"),
        "fuentes": (PROJECT_PATHS["used_sources"], "matriz de fuentes usadas"),
        "calidad": (PROJECT_PATHS["quality"], "evaluaciones de calidad"),
        "extraccion": (PROJECT_PATHS["extraction"], "datos extraídos"),
        "sintesis": (PROJECT_PATHS["evidence_map"], "mapa de evidencia"),
    }
    for phase, (relative, label) in phase_artifacts.items():
        status = state.get("phases", {}).get(phase, {}).get("status")
        if status == "completed" and csv_data_rows(root / relative) == 0:
            severe_errors.append(
                f"La fase {phase} figura completa, pero no contiene {label}."
            )

    if state.get("phases", {}).get("protocolo", {}).get("status") == "completed":
        protocol = (root / PROJECT_PATHS["protocol"]).read_text(encoding="utf-8")
        if "Pendiente" in protocol:
            warnings.append(
                "El protocolo figura completo, pero conserva marcadores 'Pendiente'."
            )

    completed = [
        phase
        for phase, info in state.get("phases", {}).items()
        if info.get("status") == "completed"
    ]
    snapshots = list((root / "10_respaldo/02_snapshots").glob("*.zip"))
    if completed and not snapshots:
        severe_errors.append("Hay fases completadas sin ningún snapshot.")
    severe_errors.extend(layout_violations(root))

    metrics = coverage_metrics(root, config)
    severe_errors.extend(
        f"Fuente incluida sin descarga y revisión válidas: {issue}"
        for issue in metrics["included_download_issues"]
    )
    severe_errors.extend(
        f"Fuente usada sin descarga y revisión válidas: {issue}"
        for issue in metrics["used_source_issues"]
    )
    if metrics["unreviewed_evidence_study_ids"]:
        severe_errors.append(
            "Calidad, extracción o síntesis usan estudios sin texto completo "
            "local revisado: "
            + ", ".join(metrics["unreviewed_evidence_study_ids"])
            + "."
        )
    if metrics["citation_unknown_source_ids"]:
        severe_errors.append(
            "La auditoría de citas contiene fuentes no registradas como usadas: "
            + ", ".join(metrics["citation_unknown_source_ids"])
            + "."
        )
    if "informe" in completed:
        missing_citation_audits = sorted(
            set(metrics["used_source_ids"])
            - set(metrics["verified_citation_source_ids"]),
            key=str.casefold,
        )
        if missing_citation_audits:
            severe_errors.append(
                "El informe está cerrado sin verificación manual contra el "
                "archivo local para estas fuentes: "
                + ", ".join(missing_citation_audits)
                + "."
            )
    if "busqueda" in completed:
        if metrics["search_traceability_gaps"]:
            severe_errors.append(
                "La búsqueda cerrada no es reproducible por campos incompletos."
            )
        if metrics["unregistered_export_sources"]:
            severe_errors.append(
                "La búsqueda cerrada carece de exportaciones brutas inventariadas."
            )
    sync_generated_outputs(root, metrics)
    assessment = control_assessment(metrics, severe_errors)

    exception_rows = read_csv(root / PROJECT_PATHS["exceptions"])
    draft_exceptions = [
        row.get("exception_id", "")
        for row in exception_rows
        if normalized(row.get("status")) == "draft"
    ]
    if draft_exceptions:
        warnings.append(
            "Excepciones metodológicas pendientes de completar: "
            + ", ".join(draft_exceptions)
            + "."
        )
    if metrics["included_without_valid_year"]:
        warnings.append(
            "Estudios incluidos sin año válido: "
            f"{metrics['included_without_valid_year']}."
        )
    warnings.extend(
        f"Fase pendiente: {phase}"
        for phase, info in state.get("phases", {}).items()
        if info.get("status") == "pending"
    )

    stamp = now_stamp()
    audited_at = now_iso()
    public_metrics = dict(metrics)
    public_metrics.pop("marginal_contribution", None)
    payload = {
        "project": str(root),
        "methodology": config.get("methodology"),
        "audited_at": audited_at,
        "control_status": assessment["status"],
        "ok": assessment["status"] != "BLOCKED",
        "severe_errors": severe_errors,
        "coverage_issues": assessment["coverage_issues"],
        "advisory_signals": assessment["advisory_signals"],
        "external_requirement_failures": (
            assessment["external_requirement_failures"]
        ),
        "warnings": warnings,
        "checks": checks,
        "coverage": public_metrics,
        "inventory_records": csv_data_rows(inventory),
        "snapshots": len(snapshots),
    }

    coverage_dir = root / "09_auditorias/02_cobertura"
    coverage_json = coverage_dir / f"09-02_suficiencia-{stamp}.json"
    coverage_md = coverage_dir / f"09-02_suficiencia-{stamp}.md"
    write_json(coverage_json, payload)
    lines = [
        "# Evaluación De Suficiencia De Cobertura",
        "",
        f"- Estado: `{assessment['status']}`",
        f"- Fuentes ejecutadas: {metrics['executed_sources']} "
        "(cantidad descriptiva, no puerta universal)",
        f"- Fuente multidisciplinaria: "
        f"{'Sí' if metrics['has_multidisciplinary_source'] else 'No'}",
        f"- Fuente especializada: "
        f"{'Sí' if metrics['has_domain_specialized_source'] else 'No'}",
        f"- Complemento independiente o justificado: "
        f"{'Sí' if metrics['has_independent_complement'] or metrics['complement_absence_justified'] else 'No'}",
        f"- Backward snowballing: "
        f"{'Sí' if metrics['backward_snowballing_done'] else 'No'}",
        f"- Forward snowballing: "
        f"{'Sí' if metrics['forward_snowballing_done'] else 'No'}",
        f"- Semillas recuperadas: {metrics['seed_articles_recovered']}/"
        f"{metrics['seed_articles_available']}",
        f"- Registros únicos: {metrics['candidates_after_dedup']}",
        f"- Textos completos evaluados: {metrics['fulltexts_assessed']}",
        f"- Textos completos locales revisados: {metrics['reviewed_fulltexts']}",
        f"- Estudios incluidos: {metrics['included_studies']}",
        f"- Fuentes usadas locales y revisadas: {metrics['reviewed_used_sources']}",
        f"- Evidencia reciente: {metrics['recent_evidence_percentage']:.1f}%",
        f"- Última búsqueda: {metrics['latest_search_date'] or 'No registrada'}",
        "",
        "## Problemas De Cobertura",
        "",
    ]
    lines.extend(
        f"- {item}" for item in assessment["coverage_issues"] or ["Ninguno."]
    )
    lines.extend(["", "## Señales Advisory", ""])
    lines.extend(
        f"- {item}" for item in assessment["advisory_signals"] or ["Ninguna."]
    )
    lines.extend(["", "## Requisitos Externos", ""])
    lines.extend(
        f"- {item}"
        for item in assessment["external_requirement_failures"] or ["Ninguno."]
    )
    lines.extend(["", "## Errores Graves", ""])
    lines.extend(f"- {item}" for item in severe_errors or ["Ninguno."])
    coverage_md.parent.mkdir(parents=True, exist_ok=True)
    atomic_write(coverage_md, "\n".join(lines) + "\n", overwrite=True)
    payload["coverage_report"] = str(coverage_md)

    report_dir = root / "09_auditorias/01_integridad"
    json_path = report_dir / f"09-01_auditoria-{stamp}.json"
    md_path = report_dir / f"09-01_auditoria-{stamp}.md"
    write_json(json_path, payload)
    audit_lines = [
        "# Auditoría Kitchenham",
        "",
        f"- Proyecto: `{root}`",
        f"- Fecha: {audited_at}",
        f"- Estado de control: `{assessment['status']}`",
        f"- Archivos inventariados: {payload['inventory_records']}",
        f"- Snapshots: {payload['snapshots']}",
        "",
        "## Errores Graves",
        "",
    ]
    audit_lines.extend(f"- {item}" for item in severe_errors or ["Ninguno."])
    audit_lines.extend(["", "## Advertencias", ""])
    audit_lines.extend(f"- {item}" for item in warnings or ["Ninguna."])
    atomic_write(md_path, "\n".join(audit_lines) + "\n", overwrite=True)
    append_log(
        root,
        "auditoria",
        "completed" if assessment["status"] in {"PASS", "PASS_WITH_WARNINGS"} else "in_progress",
        "Auditoría ejecutada",
        assessment["status"],
    )
    print(json.dumps({"report": str(md_path), **payload}, ensure_ascii=False))
    return 1 if assessment["status"] == "BLOCKED" else 0


def show_status(args: argparse.Namespace) -> int:
    root = require_project(Path(args.project_dir))
    state = read_json(root / PROJECT_PATHS["state"])
    config = effective_config(read_json(root / PROJECT_PATHS["config"]))
    metrics = coverage_metrics(root, config)
    source_errors = [
        *[
            f"Fuente incluida sin descarga y revisión válidas: {item}"
            for item in metrics["included_download_issues"]
        ],
        *[
            f"Fuente usada sin descarga y revisión válidas: {item}"
            for item in metrics["used_source_issues"]
        ],
    ]
    if metrics["unreviewed_evidence_study_ids"]:
        source_errors.append(
            "Se usan estudios sin texto completo local revisado: "
            + ", ".join(metrics["unreviewed_evidence_study_ids"])
            + "."
        )
    if metrics["citation_unknown_source_ids"]:
        source_errors.append(
            "La auditoría de citas contiene fuentes no registradas como usadas: "
            + ", ".join(metrics["citation_unknown_source_ids"])
            + "."
        )
    if state.get("phases", {}).get("informe", {}).get("status") == "completed":
        missing_citation_audits = sorted(
            set(metrics["used_source_ids"])
            - set(metrics["verified_citation_source_ids"]),
            key=str.casefold,
        )
        if missing_citation_audits:
            source_errors.append(
                "Falta verificación manual contra archivo local para: "
                + ", ".join(missing_citation_audits)
                + "."
            )
    assessment = control_assessment(metrics, source_errors)
    public_metrics = dict(metrics)
    public_metrics.pop("marginal_contribution", None)
    print(
        json.dumps(
            {
                "title": config.get("title"),
                "methodology": config.get("methodology"),
                "project": str(root),
                "control_status": assessment["status"],
                "assessment": assessment,
                "phases": state.get("phases"),
                "coverage": public_metrics,
                "inventory_records": csv_data_rows(
                    root / PROJECT_PATHS["inventory"]
                ),
                "snapshots": len(
                    list((root / "10_respaldo/02_snapshots").glob("*.zip"))
                ),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Gestiona trazabilidad, suficiencia y respaldos Kitchenham."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Inicializa un proyecto Kitchenham.")
    init_parser.add_argument("--project-dir", required=True)
    init_parser.add_argument("--title", required=True)
    init_parser.add_argument("--topic", required=True)
    init_parser.add_argument("--question", required=True)
    init_parser.add_argument("--citation-style", default="apa7")
    init_parser.add_argument("--year-start", type=int)
    init_parser.add_argument("--year-end", type=int)
    init_parser.add_argument("--languages", default="español;inglés")
    init_parser.add_argument("--disciplines", default="")
    init_parser.add_argument("--databases", default="")
    init_parser.add_argument(
        "--expected-unique-records",
        "--min-candidates",
        dest="expected_unique_records",
        type=int,
        default=300,
    )
    init_parser.add_argument(
        "--expected-fulltexts",
        "--min-fulltexts",
        dest="expected_fulltexts",
        type=int,
        default=100,
    )
    init_parser.add_argument(
        "--expected-included",
        "--min-included",
        dest="expected_included",
        type=int,
        default=50,
    )
    init_parser.add_argument("--recent-years", type=int, default=5)
    init_parser.add_argument(
        "--expected-recent-percentage",
        "--min-recent-share",
        dest="expected_recent_percentage",
        type=float,
        default=60.0,
    )
    init_parser.add_argument(
        "--threshold-enforcement",
        choices=["advisory", "external_requirement"],
        default="advisory",
    )
    init_parser.add_argument("--requirement-source", default="")
    init_parser.add_argument("--recommended-sources-min", type=int, default=4)
    init_parser.add_argument("--recommended-sources-max", type=int, default=5)
    init_parser.add_argument("--seed-articles-min", type=int, default=5)
    init_parser.add_argument("--seed-articles-max", type=int, default=10)
    init_parser.add_argument("--seed-recovery-target", type=float, default=90.0)
    init_parser.add_argument(
        "--marginal-warning-percentage",
        type=float,
        default=1.0,
    )
    init_parser.add_argument("--seed-articles-unavailable", action="store_true")
    init_parser.add_argument("--seed-unavailability-justification", default="")
    init_parser.add_argument(
        "--recommended-search-age-days",
        "--max-search-age-days",
        dest="recommended_search_age_days",
        type=int,
        default=90,
    )
    init_parser.add_argument(
        "--search-update-enforcement",
        choices=["advisory", "external_requirement"],
        default="advisory",
    )
    init_parser.set_defaults(func=create_project)

    register_parser = subparsers.add_parser(
        "register-source",
        help="Copia, clasifica e inventaría una fuente.",
    )
    register_parser.add_argument("--project-dir", required=True)
    register_parser.add_argument("--file", required=True)
    register_parser.add_argument(
        "--kind",
        choices=["search-export", "fulltext", "supplement", "metadata", "other"],
        required=True,
    )
    register_parser.add_argument(
        "--decision",
        choices=["included", "excluded", "pending", "not-applicable"],
        default="pending",
    )
    register_parser.add_argument("--database", default="")
    register_parser.add_argument("--query-id", default="")
    register_parser.add_argument("--origin", default="")
    register_parser.add_argument("--source-id", default="")
    register_parser.add_argument("--study-id", default="")
    register_parser.add_argument(
        "--source-role",
        choices=[
            "primary-study",
            "secondary-study",
            "methodological",
            "background",
            "other",
        ],
        default="primary-study",
    )
    register_parser.add_argument("--title", default="")
    register_parser.add_argument("--doi", default="")
    register_parser.add_argument("--url", default="")
    register_parser.add_argument("--content-reviewed", action="store_true")
    register_parser.add_argument("--citations-reviewed", action="store_true")
    register_parser.add_argument("--reviewed-by", default="")
    register_parser.add_argument("--reviewed-at", default="")
    register_parser.add_argument("--exclusion-reason", default="")
    register_parser.set_defaults(func=register_source)

    review_parser = subparsers.add_parser(
        "review-source",
        help=(
            "Registra la revisión manual y clasifica un texto completo "
            "inventariado."
        ),
    )
    review_parser.add_argument("--project-dir", required=True)
    review_parser.add_argument("--record-id", required=True)
    review_parser.add_argument(
        "--decision",
        choices=["included", "excluded"],
        required=True,
    )
    review_parser.add_argument("--content-reviewed", action="store_true")
    review_parser.add_argument("--citations-reviewed", action="store_true")
    review_parser.add_argument("--reviewed-by", required=True)
    review_parser.add_argument("--reviewed-at", default="")
    review_parser.add_argument("--exclusion-reason", default="")
    review_parser.set_defaults(func=review_source)

    phase_parser = subparsers.add_parser(
        "phase",
        help="Actualiza una fase y crea respaldo.",
    )
    phase_parser.add_argument("--project-dir", required=True)
    phase_parser.add_argument("--phase", choices=PHASES, required=True)
    phase_parser.add_argument(
        "--status",
        choices=["pending", "in_progress", "completed", "blocked"],
        required=True,
    )
    phase_parser.add_argument("--note", default="")
    phase_parser.add_argument("--no-snapshot", action="store_true")
    phase_parser.set_defaults(func=update_phase)

    snapshot_parser = subparsers.add_parser("snapshot", help="Crea manifiesto y ZIP.")
    snapshot_parser.add_argument("--project-dir", required=True)
    snapshot_parser.add_argument("--phase", choices=PHASES, required=True)
    snapshot_parser.add_argument("--note", default="")
    snapshot_parser.set_defaults(func=snapshot_command)

    search_audit_parser = subparsers.add_parser(
        "search-audit",
        help="Registra la auditoría metodológica activada por señales de cobertura.",
    )
    search_audit_parser.add_argument("--project-dir", required=True)
    search_audit_parser.add_argument(
        "--decision",
        choices=[
            "keep-protocol",
            "correct-strings",
            "add-source",
            "expand-vocabulary",
            "modify-period",
            "amend-scope",
            "methodological-exception",
        ],
        required=True,
    )
    search_audit_parser.add_argument("--reviewed-by", required=True)
    search_audit_parser.add_argument("--review-notes", required=True)
    search_audit_parser.set_defaults(func=record_search_audit)

    exception_parser = subparsers.add_parser(
        "methodological-exception",
        help="Completa una excepción metodológica trazable.",
    )
    exception_parser.add_argument("--project-dir", required=True)
    exception_parser.add_argument("--exception-id", required=True)
    exception_parser.add_argument("--threshold", required=True)
    exception_parser.add_argument("--expected", required=True)
    exception_parser.add_argument("--obtained", required=True)
    exception_parser.add_argument("--responsible", required=True)
    exception_parser.add_argument("--reviews-performed", required=True)
    exception_parser.add_argument("--changes-applied", required=True)
    exception_parser.add_argument("--justification", required=True)
    exception_parser.add_argument("--risk", required=True)
    exception_parser.add_argument("--impact", required=True)
    exception_parser.add_argument("--decision", required=True)
    exception_parser.add_argument("--approved-by", required=True)
    exception_parser.set_defaults(func=record_methodological_exception)

    audit_parser = subparsers.add_parser(
        "audit",
        help="Audita integridad, suficiencia y señales operativas.",
    )
    audit_parser.add_argument("--project-dir", required=True)
    audit_parser.set_defaults(func=audit_project)

    status_parser = subparsers.add_parser("status", help="Muestra estado y cobertura.")
    status_parser.add_argument("--project-dir", required=True)
    status_parser.set_defaults(func=show_status)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
