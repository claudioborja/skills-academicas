#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import sys
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'editor-en-jefe/scripts'))
from archivos_seguros import atomic_write, validate_outputs
from typing import Any

from common import read_records, write_json


METHODOLOGIES: dict[str, dict[str, Any]] = {
    "revision_sistematica": {
        "label": "Revision sistematica",
        "guide": "PRISMA 2020",
        "question": "PICO/PICOS o PECO",
        "when": "Pregunta focalizada, busqueda reproducible, criterios de inclusion/exclusion, cribado y sintesis transparente.",
        "checklist": [
            "formular pregunta y criterios antes de buscar",
            "definir bases de datos, cadenas, fechas e idiomas",
            "registrar cribado y razones de exclusion",
            "extraer datos en matriz trazable",
            "reportar diagrama de flujo y limitaciones",
        ],
    },
    "scoping_review": {
        "label": "Revision de alcance",
        "guide": "PRISMA-ScR + JBI/PCC",
        "question": "PCC: poblacion, concepto, contexto",
        "when": "Tema amplio o emergente que necesita mapear conceptos, tipos de evidencia, contextos y vacios.",
        "checklist": [
            "delimitar poblacion, concepto y contexto",
            "mapear tipos de estudio y fuentes",
            "clasificar lineas, brechas y definiciones",
            "evitar conclusiones de efecto si no hay evaluacion apropiada",
        ],
    },
    "metaanalisis": {
        "label": "Revision sistematica con metaanalisis",
        "guide": "PRISMA 2020 + plan estadistico del area",
        "question": "PICO/PICOS",
        "when": "Hay estudios comparables, medidas de efecto compatibles y suficiente homogeneidad conceptual.",
        "checklist": [
            "definir desenlaces y medidas de efecto",
            "evaluar heterogeneidad",
            "prever analisis de sensibilidad o subgrupos",
            "reportar modelo estadistico y sesgo de publicacion si aplica",
        ],
    },
    "revision_narrativa": {
        "label": "Revision narrativa o integrativa",
        "guide": "Marco explicito propio; transparencia inspirada en PRISMA cuando sea util",
        "question": "Pregunta conceptual o integrativa",
        "when": "Sintesis teorica amplia, literatura heterogenea o argumento conceptual que no promete exhaustividad sistematica.",
        "checklist": [
            "declarar alcance y criterio de seleccion",
            "separar evidencia empirica de interpretacion",
            "hacer trazables las fuentes clave",
            "no afirmar exhaustividad si no hubo protocolo sistematico",
        ],
    },
    "observacional": {
        "label": "Estudio observacional",
        "guide": "STROBE",
        "question": "PECO/PICO observacional",
        "when": "Cohorte, caso-control, transversal, encuesta, base secundaria o analisis de asociaciones.",
        "checklist": [
            "definir diseno, escenario, participantes y variables",
            "explicar sesgos y tamano muestral",
            "describir metodos estadisticos",
            "reportar resultados principales y limitaciones",
        ],
    },
    "ensayo": {
        "label": "Ensayo o intervencion aleatorizada",
        "guide": "CONSORT 2025",
        "question": "PICO",
        "when": "Intervencion con asignacion aleatoria, comparador, desenlaces predefinidos y flujo de participantes.",
        "checklist": [
            "definir intervencion, comparador y desenlaces",
            "describir aleatorizacion y cegamiento si aplica",
            "reportar flujo de participantes",
            "separar analisis primario, secundarios y eventos adversos",
        ],
    },
    "cualitativo": {
        "label": "Estudio cualitativo",
        "guide": "COREQ o SRQR",
        "question": "SPIDER o pregunta cualitativa",
        "when": "Entrevistas, grupos focales, observacion, analisis tematico, fenomenologia o teoria fundamentada.",
        "checklist": [
            "explicar posicionamiento, muestreo y contexto",
            "describir recoleccion y analisis",
            "mostrar trazabilidad entre datos, categorias e interpretacion",
            "cuidar criterios eticos y saturacion cuando aplique",
        ],
    },
    "diagnostico": {
        "label": "Estudio de exactitud diagnostica",
        "guide": "STARD",
        "question": "PIRD",
        "when": "Evalua sensibilidad, especificidad o desempeno de una prueba indice frente a referencia.",
        "checklist": [
            "definir prueba indice y estandar de referencia",
            "describir participantes y flujo",
            "reportar estimaciones con incertidumbre",
            "discutir aplicabilidad y sesgos",
        ],
    },
    "predictivo": {
        "label": "Modelo predictivo o pronostico",
        "guide": "TRIPOD",
        "question": "PICO/objetivo predictivo",
        "when": "Desarrolla, valida o actualiza un modelo de prediccion o pronostico.",
        "checklist": [
            "definir desenlace, predictores y fuente de datos",
            "separar desarrollo y validacion",
            "reportar desempeno, calibracion y manejo de datos faltantes",
            "evitar sobreprometer utilidad clinica o practica sin validacion",
        ],
    },
    "caso": {
        "label": "Reporte o serie de casos",
        "guide": "CARE",
        "question": "Pregunta clinica o caso significativo",
        "when": "Caso unico o serie breve con valor descriptivo, diagnostico, terapeutico o pedagogico.",
        "checklist": [
            "presentar linea temporal",
            "describir diagnostico, intervencion y desenlace",
            "explicar singularidad y limites",
            "proteger datos identificables",
        ],
    },
    "protocolo": {
        "label": "Protocolo",
        "guide": "PRISMA-P para revisiones; SPIRIT para ensayos",
        "question": "PICO/PICOS segun diseno",
        "when": "Plan previo antes de ejecutar una revision sistematica o ensayo/intervencion.",
        "checklist": [
            "declarar objetivos, criterios y plan de analisis",
            "registrar cambios posteriores",
            "definir cronograma y roles",
            "prever estrategia de manejo de datos",
        ],
    },
}


GOAL_ALIASES = {
    "revision": "revision_sistematica",
    "systematic-review": "revision_sistematica",
    "revision-sistematica": "revision_sistematica",
    "scoping": "scoping_review",
    "scoping-review": "scoping_review",
    "alcance": "scoping_review",
    "meta-analysis": "metaanalisis",
    "metaanalisis": "metaanalisis",
    "narrativa": "revision_narrativa",
    "integrativa": "revision_narrativa",
    "original-observational": "observacional",
    "observacional": "observacional",
    "ensayo": "ensayo",
    "trial": "ensayo",
    "cualitativo": "cualitativo",
    "qualitative": "cualitativo",
    "diagnostico": "diagnostico",
    "diagnostic": "diagnostico",
    "predictivo": "predictivo",
    "prediction": "predictivo",
    "caso": "caso",
    "case": "caso",
    "protocolo": "protocolo",
    "protocol": "protocolo",
}


KEYWORDS = {
    "revision_sistematica": ["systematic review", "prisma", "screening", "eligibility", "revision sistematica"],
    "scoping_review": ["scoping", "scope", "pcc", "mapping review", "alcance"],
    "metaanalisis": ["meta-analysis", "meta analysis", "metaanalisis", "effect size", "heterogeneity"],
    "revision_narrativa": ["narrative review", "integrative review", "conceptual", "theoretical", "narrativa"],
    "observacional": ["cross-sectional", "cohort", "case-control", "survey", "encuesta", "observational", "transversal"],
    "ensayo": ["randomized", "randomised", "trial", "control group", "intervention", "aleatorizado", "ensayo"],
    "cualitativo": ["interview", "focus group", "qualitative", "thematic analysis", "entrevista", "cualitativo"],
    "diagnostico": ["diagnostic", "sensitivity", "specificity", "accuracy", "diagnostico"],
    "predictivo": ["prediction", "predictive", "prognostic", "machine learning", "model validation", "prediccion"],
    "caso": ["case report", "case study", "series of cases", "estudio de caso", "reporte de caso"],
    "protocolo": ["protocol", "prisma-p", "spirit", "protocolo"],
}


TYPE_TO_METHOD = {
    "revision": "revision_sistematica",
    "original": "observacional",
    "metodologico": "predictivo",
    "caso": "caso",
    "teorico": "revision_narrativa",
}


def all_text(records: list[dict[str, Any]]) -> str:
    return "\n".join(" ".join(str(v) for v in row.values() if v is not None) for row in records).lower()


def build_result(key: str, reason: str, records: list[dict[str, Any]]) -> dict[str, Any]:
    item = METHODOLOGIES[key]
    counts = collections.Counter(str(row.get("article_type", "sin_tipo") or "sin_tipo") for row in records)
    return {
        "recommended_key": key,
        "recommended_methodology": item["label"],
        "reporting_guideline": item["guide"],
        "question_framework": item["question"],
        "when_to_use": item["when"],
        "minimum_checklist": item["checklist"],
        "reason": reason,
        "records": len(records),
        "article_type_counts": dict(counts),
        "next_scripts": [
            "clasificar_literatura.py",
            "matriz_estado_arte.py",
            "proponer_temas.py",
            "tabular_visualizar.py",
        ],
        "caution": "Verificar instrucciones de la revista y no declarar cumplimiento de una guia si el diseno no cumple sus requisitos.",
    }


def choose(records: list[dict[str, Any]], goal: str | None) -> dict[str, Any]:
    if goal:
        key = GOAL_ALIASES.get(goal.strip().lower(), goal.strip().lower().replace("-", "_"))
        if key in METHODOLOGIES:
            return build_result(key, "Seleccion directa por --goal.", records)
        raise SystemExit(f"--goal no reconocido: {goal}")

    text = all_text(records)
    scores: collections.Counter[str] = collections.Counter()
    for key, clues in KEYWORDS.items():
        for clue in clues:
            if clue in text:
                scores[key] += 2 if " " in clue else 1

    article_types = collections.Counter(str(row.get("article_type", "")).strip().lower() for row in records)
    for article_type, count in article_types.items():
        mapped = TYPE_TO_METHOD.get(article_type)
        if mapped:
            scores[mapped] += count

    if not scores:
        return build_result("revision_narrativa", "No hubo senales fuertes; se recomienda marco narrativo/integrativo hasta precisar datos.", records)

    key, score = scores.most_common(1)[0]
    return build_result(key, f"Heuristica por senales del corpus; puntaje {score}.", records)


def render(result: dict[str, Any]) -> str:
    lines = [
        "# Seleccion metodologica",
        "",
        f"- Metodologia recomendada: {result['recommended_methodology']}",
        f"- Guia de reporte: {result['reporting_guideline']}",
        f"- Marco de pregunta: {result['question_framework']}",
        f"- Registros evaluados: {result['records']}",
        f"- Razon: {result['reason']}",
        "",
        "## Cuando usarla",
        "",
        result["when_to_use"],
        "",
        "## Checklist minimo",
        "",
    ]
    lines.extend(f"- {item}" for item in result["minimum_checklist"])
    lines.extend(["", "## Distribucion detectada", ""])
    for key, value in sorted(result["article_type_counts"].items()):
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Siguientes scripts", ""])
    lines.extend(f"- `{item}`" for item in result["next_scripts"])
    lines.extend(["", "## Cautela", "", result["caution"], ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Selecciona metodologia/guia de reporte segun corpus u objetivo.")
    parser.add_argument("input", help="CSV, JSON, Markdown o TXT con literatura o clasificacion previa.")
    parser.add_argument("--goal", help="Opcional: revision, scoping, metaanalisis, observacional, ensayo, cualitativo, diagnostico, predictivo, caso, protocolo.")
    parser.add_argument("--out", help="Ruta Markdown de salida.")
    parser.add_argument("--json-out", help="Ruta JSON de salida.")
    parser.add_argument('--overwrite', action='store_true', help='Reemplazar informes existentes, nunca entradas')
    args = parser.parse_args()
    try:
        validate_outputs([args.input], [args.out, args.json_out], args.overwrite)
    except ValueError as exc:
        parser.error(str(exc))

    result = choose(read_records(args.input), args.goal)
    report = render(result)
    if args.out:
        atomic_write(args.out, report, overwrite=args.overwrite)
    else:
        sys.stdout.write(report)
    if args.json_out:
        write_json(args.json_out, result, overwrite=args.overwrite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
