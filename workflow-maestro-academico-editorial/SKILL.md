---
name: workflow-maestro-academico-editorial
description: Coordina las skills académicas y editoriales según el producto y la etapa del manuscrito. Usar para organizar proyectos de libro, tesis, artículo o revisión y seleccionar apoyos sin duplicar intervenciones.
---

# Workflow Maestro Académico Editorial

## Responsabilidad

Ser la entrada de coordinación de esta colección. Identificar producto, etapa, encargo, método, norma y materiales disponibles; activar únicamente las especialidades necesarias. Una corrección breve no requiere ejecutar el flujo completo ni crear un proyecto de libro.

Consultar [references/mapa-responsabilidades.md](references/mapa-responsabilidades.md) para elegir la skill y sus límites. Cada script especializado pertenece a su skill; el lanzador general está en `scripts/ejecutar.py`.

## Reglas compartidas

El lanzador comprueba colisiones de entrada/salida y salidas existentes para `--out`, `--json-out`, `--report`, `--csv-out` y `--backup`. Para reemplazar una salida, usar `--permitir-sobrescritura` antes del script; nunca autoriza reemplazar entradas. Esta comprobación es preventiva, no un aislamiento del programa: opciones no reconocidas, directorios y escrituras internas necesitan validación propia. `scripts/archivos_seguros.py` centraliza validación y escritura atómica para herramientas que lo integran.

- Aplicar [references/perfiles-editoriales.md](references/perfiles-editoriales.md) para la precedencia entre encargo, protocolo, norma y perfil. Registrar preferencias en la ficha existente del proyecto; no replicar reglas numéricas en cada skill.
- Con Kitchenham activo, su protocolo gobierna búsqueda, selección, calidad, extracción y síntesis. No activar protocolos o conteos PRISMA desde un apoyo editorial. Una enmienda debe quedar documentada.
- Proteger datos, citas textuales, transcripciones, DOI, URLs, referencias, tablas, fórmulas y código. No inventar evidencia ni completar una extensión con relleno.
- Automatizar solo operaciones deterministas reutilizables. Mantener tema, contenido del libro y preferencias autorales en datos o en el manuscrito, nunca como párrafos fijos de un programa general.
- Los inventarios, coincidencias léxicas y métricas son señales para revisión. No certifican coherencia científica, respaldo de una cita, autoría humana ni calidad editorial.
- La instrucción del usuario delimita la intervención: un diagnóstico no autoriza reescritura; una corrección de formato no autoriza cambiar fuentes o método.

## Ruta de trabajo

1. **Situar el producto.** Tesis que seguirá siendo tesis: constructor de tesis. Cambio de tesis a libro: convertidor. Artículo: IMRyD. Revisión Kitchenham: su skill metodológica.
2. **Preparar insumos si hace falta.** Para archivos largos, usar preprocesamiento y mapas de secciones. Si se necesita un inventario mecánico, activar auditor documental. Leer los pasajes necesarios para juzgar el contenido.
3. **Planificar.** Inicializar la estructura canónica solo para libros nuevos o completar una existente con `--merge`. En otros productos, respetar las carpetas del proyecto o protocolo.
4. **Investigar y redactar.** Resolver problema, objetivos, evidencia y método antes de pulir estilo. Seleccionar las skills de fuentes, marco teórico y redacción pertinentes.
5. **Revisar.** Coherencia interna, continuidad entre capítulos y terminología según el alcance; referencias, ecuaciones y recursos visuales cuando existan.
6. **Cerrar estilo y entrega.** Humanizar solo si hay genericidad o voz mecánica; después corregir ortotipografía, redactar resumen y maquetar.
7. **Responder observaciones.** Abrir una nueva ronda trazable con la skill correspondiente, sin repetir fases ya resueltas.

No ejecutar todas las etapas por rutina. Tras una edición sustancial, revisar únicamente lo que pudo verse afectado: por ejemplo, referencias y conclusiones si se cambió el argumento.

## Entregables y recursos

Usar la estructura de `$planificador-obra-academica` para libros. Conservar originales, borradores, fuentes activas/descartadas y entregables en sus destinos; documentar equivalencias en proyectos existentes.

Para Word, usar `$maquetacion-academica-preentrega`: tablas editables y salida DOCX, con TXT de respaldo cuando sea parte del encargo. La extensión y el formato dependen del perfil seleccionado; una exportación no demuestra que el resultado visual sea correcto.

Las imágenes y tablas deben aportar comprensión. La skill de imágenes gobierna procedencia, licencias y generación; la de tablas/figuras gobierna integración, títulos, numeración, llamadas y notas. No duplicar recursos por cuotas ni presentar ilustraciones como evidencia.

Cuando la obra contenga ecuaciones, activar `$gestor-ecuaciones-academicas` para preservar significado, notación, unidades, numeración, referencias y editabilidad. El auditor mecánico de esa skill no certifica equivalencia algebraica ni validez científica; la maquetación final gobierna su integración y revisión visual en Word/PDF.

Si llega un reporte de similitud/IA, usar humanización para interpretarlo con cautela y revisar prosa propia de forma selectiva. No perseguir porcentajes ni alterar contenido protegido para modificar una puntuación.

## Recursos bajo demanda

- Para mantenimiento, `scripts/validar_coleccion.py` reúne estructura, pruebas, dependencias y comparación de copias. Consultar [validación unificada](references/portabilidad.md#validación-unificada). No instala ni sincroniza archivos y no presenta pruebas omitidas como aprobación.
- Para publicar o actualizar el catálogo del repositorio, `scripts/generar_documentacion_skills.py` crea una ficha Markdown por cada skill visible a partir de su frontmatter, secciones y recursos reales. Requiere `--overwrite` para actualizar un destino existente y excluye entornos, cachés y bytecode.
- [references/portabilidad.md](references/portabilidad.md): ejecución, Python y pruebas.
- [references/perfiles-editoriales.md](references/perfiles-editoriales.md): políticas y formato del proyecto.
- [references/mapa-responsabilidades.md](references/mapa-responsabilidades.md): selección de especialidades.
- [references/ruta-de-trabajo.md](references/ruta-de-trabajo.md) y [references/diagnostico-por-etapa.md](references/diagnostico-por-etapa.md): orientación adicional por etapa.
- [references/migracion-27-skills.md](references/migracion-27-skills.md): equivalencias y recuperación tras la fusión; solo para mantenimiento.
- [references/auditoria-automatizacion.md](references/auditoria-automatizacion.md): registro histórico, no certificado de validez vigente.

## Cierre

Verificar que se atendió el encargo, las fuentes y datos conservan trazabilidad, el método no cambió por una skill auxiliar y las comprobaciones corresponden al producto entregado. Comunicar pendientes reales y límites de la validación.

