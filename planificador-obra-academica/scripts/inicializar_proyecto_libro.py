#!/usr/bin/env python3
"""Inicializar la estructura editorial canónica de un proyecto de libro."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'workflow-maestro-academico-editorial/scripts'))
from archivos_seguros import atomic_write


DIRECTORIES = (
    "00_contexto_y_diagnostico/originales",
    "00_contexto_y_diagnostico/preprocesado",
    "01_planificacion_editorial",
    "02_manuscrito",
    "03_casos_aplicados",
    "04_recursos_didacticos",
    "05_investigacion_bibliografia/fuentes_activas",
    "05_investigacion_bibliografia/fuentes_descartadas",
    "05_investigacion_bibliografia/metadata",
    "06_recursos_visuales/imagenes",
    "06_recursos_visuales/originales",
    "06_recursos_visuales/metadata",
    "06_recursos_visuales/tablas_html",
    "07_glosario_terminologia",
    "08_revision_editorial",
    "09_entregables/v01_borrador",
    "09_entregables/v02_revision",
    "09_entregables/v02_revision/anexos",
    "09_entregables/v03_final_txt",
    "09_entregables/v03_final_docx",
    "plantillas",
)


def starter_files(title: str) -> dict[str, str]:
    safe_title = title.strip() or "Proyecto de libro"
    return {
        "00_indice_maestro.md": f"""# {safe_title}\n\n## Estado\n\nProyecto inicializado. Investigación y redacción pendientes.\n\n## Ruta editorial\n\n1. Contexto y diagnóstico\n2. Planificación editorial\n3. Investigación y bibliografía\n4. Redacción del manuscrito\n5. Casos, recursos didácticos y visuales\n6. Glosario y control terminológico\n7. Revisión editorial\n8. Entregables versionados\n""",
        "01_planificacion_editorial/00_ficha_editorial.md": f"""# Ficha editorial\n\n- **Título:** {safe_title}\n- **Subtítulo:** [Pendiente]\n- **Tipo de obra:** [Pendiente]\n- **Propósito:** [Pendiente]\n- **Lector principal:** [Pendiente]\n- **Alcance y exclusiones:** [Pendiente]\n- **Perfil editorial y formato:** [Seleccionar perfil o plantilla del proyecto]\n- **Norma bibliográfica:** [APA 7, IEEE u otra indicada]\n- **Extensión estimada:** [Objetivo y límite acordados; no imponer una cuota universal]\n- **Método y protocolo:** [Si corresponde]\n- **Política de fuentes:** [DOI, fecha, acceso y tipos documentales según el perfil/protocolo]\n- **Perfil de estilo y umbrales orientativos:** [Si corresponde]\n- **Excepciones documentadas:** [Registrar autoridad y motivo]\n""",
        "01_planificacion_editorial/01_indice_maestro.md": "# Índice maestro\n\n[Definir partes, capítulos y función de cada bloque.]\n",
        "01_planificacion_editorial/02_matriz_capitulos.md": "# Matriz de capítulos\n\n| Capítulo | Propósito | Lector cambia porque | Evidencia | Caso | Recurso visual | Estado |\n|---|---|---|---|---|---|---|\n",
        "02_manuscrito/00_preliminares.md": f"# {safe_title}\n\n## Presentación\n\n[Pendiente]\n\n## Cómo usar este libro\n\n[Pendiente]\n",
        "03_casos_aplicados/00_mapa_casos.md": "# Mapa de casos aplicados\n\n| ID | Capítulo | Función | Evidencia requerida | Estado |\n|---|---|---|---|---|\n",
        "04_recursos_didacticos/00_mapa_recursos.md": "# Mapa de recursos didácticos\n\n| ID | Capítulo | Tipo | Objetivo de aprendizaje | Estado |\n|---|---|---|---|---|\n",
        "05_investigacion_bibliografia/00_matriz_evidencia.md": "# Matriz de evidencia\n\n| Capítulo | Afirmación | Fuente | DOI/URL | Pasaje de soporte | Decisión |\n|---|---|---|---|---|---|\n",
        "05_investigacion_bibliografia/01_bibliografia_en_construccion.md": "# Bibliografía en construcción\n\n[Incluir solo fuentes verificadas y realmente utilizadas.]\n",
        "06_recursos_visuales/00_plan_visual.md": "# Plan visual\n\n| ID | Capítulo | Tipo | Función | Fuente/licencia | Estado |\n|---|---|---|---|---|---|\n",
        "06_recursos_visuales/metadata/manifiesto_imagenes.jsonl": "",
        "06_recursos_visuales/metadata/manifiesto_tablas.jsonl": "",
        "07_glosario_terminologia/00_glosario_base.md": "# Glosario y terminología\n\n| Término preferido | Definición | Variantes evitadas | Fuente |\n|---|---|---|---|\n",
        "08_revision_editorial/00_control_avance.md": "# Control de avance\n\n| Etapa | Estado | Evidencia | Próxima acción |\n|---|---|---|---|\n| Planificación | Pendiente | | |\n| Investigación | Pendiente | | |\n| Redacción | Pendiente | | |\n| Revisión | Pendiente | | |\n| Preentrega | Pendiente | | |\n",
        "08_revision_editorial/01_checklist_preentrega.md": "# Checklist de preentrega\n\n- [ ] Arquitectura completa\n- [ ] Perfil formal del proyecto aplicado y documentado\n- [ ] Extensión acorde con el objetivo y los límites acordados\n- [ ] Norma bibliográfica única aplicada a citas, notas, pies y referencias\n- [ ] Citas y referencias verificadas\n- [ ] Continuidad y terminología auditadas\n- [ ] Cada imagen y tabla aporta valor explícito y no decorativo\n- [ ] Recursos externos son open access y tienen licencia verificada\n- [ ] Recursos generados declaran modelo y fecha\n- [ ] Anexo de prompts y razones completado cuando corresponde\n- [ ] Tablas y figuras trazables\n- [ ] Tablas verificadas como objetos editables en Word\n- [ ] Revisión científica y editorial completada\n- [ ] DOCX principal y TXT de respaldo generados\n",
        "09_entregables/v02_revision/anexos/anexo_prompts_recursos_generados.md": "# Anexo de prompts y razones de recursos generados\n\n[Completar únicamente cuando existan imágenes o tablas generadas con asistencia de un modelo.]\n",
        "plantillas/plantilla_capitulo.md": "# [Número y título]\n\n## Propósito\n\n## Introducción\n\n## Desarrollo\n\n## Aplicación\n\n## Caso o actividad\n\n## Recursos visuales\n\n## Conclusión y enlace\n\n## Referencias\n",
        "plantillas/plantilla_ficha_evidencia.md": "# Ficha de evidencia\n\n- **Afirmación:**\n- **Fuente:**\n- **DOI/URL:**\n- **Pasaje o resultado:**\n- **Limitaciones:**\n- **Uso previsto:**\n",
    }


def validate_target(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    if resolved == resolved.anchor or not resolved.name:
        raise ValueError("La ruta debe identificar un directorio concreto de proyecto")
    return resolved


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="Directorio raíz del libro")
    parser.add_argument("--title", required=True, help="Título editorial del libro")
    parser.add_argument("--merge", action="store_true", help="Completar sin sobrescribir archivos existentes")
    parser.add_argument("--dry-run", action="store_true", help="Mostrar operaciones sin escribir")
    args = parser.parse_args()

    project = validate_target(args.project)
    if project.exists() and not project.is_dir():
        parser.error('La ruta del proyecto no es un directorio')
    if project.exists() and any(project.iterdir()) and not args.merge:
        parser.error("El directorio existe y no está vacío; usar --merge para completar sin sobrescribir")

    files = starter_files(args.title)
    # Comprobar todo el plan antes de crear carpetas o archivos.
    for relative in (*DIRECTORIES, *files, 'estado_proyecto.json'):
        target = project / relative
        for component in (target, *target.parents):
            if component == project:
                break
            if component.is_symlink():
                parser.error(f'No se admite un enlace simbólico en la estructura: {component}')
        if target.exists():
            is_directory = relative in DIRECTORIES
            if (is_directory and not target.is_dir()) or (not is_directory and not target.is_file()):
                parser.error(f'Tipo de archivo incompatible con la estructura: {target}')

    operations: list[dict[str, str]] = []
    for relative in DIRECTORIES:
        target = project / relative
        if not target.exists():
            operations.append({"action": "mkdir", "path": str(target)})
            if not args.dry_run:
                target.mkdir(parents=True, exist_ok=True)

    for relative, content in files.items():
        target = project / relative
        if target.exists():
            continue
        operations.append({"action": "create", "path": str(target)})
        if not args.dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            atomic_write(target, content)

    state_path = project / "estado_proyecto.json"
    if not state_path.exists():
        state = {
            "titulo": args.title.strip(),
            "fecha_inicializacion": date.today().isoformat(),
            "estructura_version": "1.2",
            "etapa_actual": "planificacion",
        }
        operations.append({"action": "create", "path": str(state_path)})
        if not args.dry_run:
            state_path.parent.mkdir(parents=True, exist_ok=True)
            atomic_write(state_path, json.dumps(state, ensure_ascii=False, indent=2) + "\n")

    print(json.dumps({"project": str(project), "dry_run": args.dry_run, "operations": operations}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
