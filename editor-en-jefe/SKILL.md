---
name: editor-en-jefe
description: Coordina las skills académicas y editoriales según el producto y la etapa del manuscrito. Usar para organizar proyectos de libro, tesis, artículo o revisión y seleccionar apoyos sin duplicar intervenciones.
---

# Editor en jefe

## Responsabilidad

Ser la entrada de coordinación de esta colección. Identificar producto, etapa, encargo, método, norma y materiales disponibles; activar únicamente las especialidades necesarias. Una corrección breve no requiere ejecutar el flujo completo ni crear un proyecto de libro.

Consultar [references/mapa-responsabilidades.md](references/mapa-responsabilidades.md) para elegir la skill y sus límites. Cada script especializado pertenece a su skill; el lanzador general está en `scripts/ejecutar.py`.

## Reglas compartidas

El lanzador comprueba colisiones de entrada/salida y salidas existentes para `--out`, `--json-out`, `--report`, `--csv-out` y `--backup`. Para reemplazar una salida, usar `--permitir-sobrescritura` antes del script; nunca autoriza reemplazar entradas. Esta comprobación es preventiva, no un aislamiento del programa: opciones no reconocidas, directorios y escrituras internas necesitan validación propia. `scripts/archivos_seguros.py` centraliza validación y escritura atómica para herramientas que lo integran.

- Aplicar [references/perfiles-editoriales.md](references/perfiles-editoriales.md) para la precedencia entre encargo, protocolo, norma y perfil. Registrar preferencias en la ficha existente del proyecto; no replicar reglas numéricas en cada skill.
- Con Kitchenham activo, su protocolo gobierna búsqueda, selección, calidad, extracción y síntesis. No activar protocolos o conteos PRISMA desde un apoyo editorial. Una enmienda debe quedar documentada.
- Con PRISMA activo, distinguir el método de conducción de la guía de reporte. Activar `$revision-sistematica-prisma` para PRISMA 2020 y sus extensiones; no presentarlo como sustituto de Kitchenham u otro método disciplinar.
- Para contribuciones o autoría, activar `$gestor-contribuciones-autoria`: CRediT describe tareas, la política del destino decide elegibilidad y responsabilidad, y JATS/Crossref/DataCite/ORCID u otros formatos solo representan metadatos.
- Proteger datos, citas textuales, transcripciones, DOI, URLs, referencias, tablas, fórmulas y código. No inventar evidencia ni completar una extensión con relleno.
- Automatizar solo operaciones deterministas reutilizables. Mantener tema, contenido del libro y preferencias autorales en datos o en el manuscrito, nunca como párrafos fijos de un programa general.
- Los inventarios, coincidencias léxicas y métricas son señales para revisión. No certifican coherencia científica, respaldo de una cita, autoría humana ni calidad editorial.
- La instrucción del usuario delimita la intervención: un diagnóstico no autoriza reescritura; una corrección de formato no autoriza cambiar fuentes o método.

## Ruta de trabajo

Para producir un libro completo, aplicar [producción editorial integrada](references/produccion-editorial-eficiente.md): controles durante la redacción, reutilización de evidencia y revisión global final. El objetivo de ahorro exige calidad conservada y tokens totales no superiores, medidos; no prometerlo por simplificar carpetas o reducir llamadas.

El archivo de contexto es opcional. Sin él, trabajar con el encargo del usuario, el manuscrito, el índice y las decisiones existentes; completar únicamente los supuestos necesarios y registrarlos en la planificación cuando corresponda. No exigir un archivo de contexto ni crear uno como requisito para avanzar. Preguntar solo por decisiones que afecten materialmente al resultado y no puedan inferirse. Los controles de coherencia, separación entre instrucciones y contenido, y presentación se aplican con o sin contexto.

Cuando se reciba un contexto maestro, ficha editorial o documento de tipo de obra, aplicar primero [interpretación del contexto editorial](references/interpretacion-contexto-editorial.md). Separar estructura publicable, instrucciones de desarrollo y controles de calidad. Entregar esa separación al planificador y a las skills de redacción y revisión; ninguna debe convertir una lista de instrucciones en el índice por defecto.

Leer todas sus secciones y mantener una matriz de requisitos con origen, ámbito, destino y evidencia. Incluir propósito, identidad, alcance, objetivos, lector, enfoque, convenciones, recursos, proceso y resultado esperado. Transmitir también la jerarquía y presentación acordadas a redacción y preentrega; el checklist final no sustituye la comprobación del contexto completo.

1. **Situar el producto.** Tesis que seguirá siendo tesis: constructor de tesis. Cambio de tesis a libro: convertidor. Artículo: IMRyD. Revisión Kitchenham: su skill metodológica. Revisión que debe reportarse con PRISMA: skill PRISMA y método de conducción declarado por separado.
2. **Preparar insumos si hace falta.** Para archivos largos, usar preprocesamiento y mapas de secciones. Si se necesita un inventario mecánico, activar auditor documental. Leer los pasajes necesarios para juzgar el contenido.
3. **Planificar.** Elegir con el planificador una estructura proporcional; crear carpetas cuando hagan falta. La estructura completa y su inicializador son opcionales. Respetar las carpetas de proyectos existentes y protocolos.
4. **Investigar y redactar.** Resolver problema, objetivos, evidencia y método antes de pulir estilo. Seleccionar las skills de fuentes, marco teórico y redacción pertinentes.
5. **Revisar.** Coherencia interna, continuidad entre capítulos y terminología según el alcance; referencias, ecuaciones y recursos visuales cuando existan. Si la obra requiere declaración de contribuciones o decisión de autoría, resolverla con la política del destino y `$gestor-contribuciones-autoria` antes de la entrega.
6. **Cerrar estilo y entrega.** Humanizar solo si hay genericidad o voz mecánica; después corregir ortotipografía y redactar el resumen. Si el libro requiere identidad visual y composición profesional en Word, activar `$disenador-maquetador-word`; cerrar con `$maquetacion-academica-preentrega` para comprobar requisitos y entrega.
7. **Responder observaciones.** Abrir una nueva ronda trazable con la skill correspondiente, sin repetir fases ya resueltas.

No ejecutar todas las etapas por rutina. Tras una edición sustancial, revisar únicamente lo que pudo verse afectado: por ejemplo, referencias y conclusiones si se cambió el argumento.

En libros con estructura canónica, leer al inicio y actualizar al cierre de una intervención sustantiva `01_planificacion_editorial/03_registro_editorial.md`. Debe resumir decisiones vigentes, estado de capítulos, requisitos/controles y la próxima acción, con enlaces o rutas a la evidencia. No crear ni exigir este registro para tareas breves, proyectos existentes que no lo usen o encargos sin estructura de libro.

## Entregables y recursos

Usar la estructura de `$planificador-obra-academica` para libros. Conservar originales, borradores, fuentes activas/descartadas y entregables en sus destinos; documentar equivalencias en proyectos existentes.

Para diseñar un libro profesional en Word, usar `$disenador-maquetador-word`: sistema visual, estilos, secciones, navegación, composición resistente al reflujo e inspección de páginas. El entregable principal continúa siendo el DOCX editable; una representación temporal en PDF puede usarse para revisar, pero no se entrega por defecto.

Usar después `$maquetacion-academica-preentrega` para verificar requisitos académicos o institucionales, limpieza y condiciones de entrega. Puede producir el DOCX inicial desde Markdown cuando sea necesario, pero no sustituye la dirección visual del libro ni debe deshacerla con valores genéricos.

Las imágenes y tablas deben aportar comprensión. La skill de imágenes gobierna procedencia, licencias y generación; la de tablas/figuras gobierna integración, títulos, numeración, llamadas y notas. No duplicar recursos por cuotas ni presentar ilustraciones como evidencia.

Cuando la obra contenga ecuaciones, activar `$gestor-ecuaciones-academicas` para preservar significado, notación, unidades, numeración, referencias y editabilidad. El auditor mecánico de esa skill no certifica equivalencia algebraica ni validez científica; la maquetación final gobierna su integración y revisión visual en Word/PDF.

Cuando un libro técnico incluya código, comandos, configuraciones o salidas de consola como contenido de lectura, activar `$gestor-codigo-tecnico-editorial`. Esa skill decide su presentación y trazabilidad; no sustituye la revisión técnica, de seguridad o de licencias del software.

Cuando deban identificarse autores, colaboradores, traductores, responsables de datos o desarrolladores, usar `$gestor-contribuciones-autoria`. No inferir autoría por cargo, número de roles CRediT u orden histórico; conservar confirmación, política aplicada y mapeo técnico.

Si llega un reporte de similitud/IA, usar humanización para interpretarlo con cautela y revisar prosa propia de forma selectiva. No perseguir porcentajes ni alterar contenido protegido para modificar una puntuación.

## Recursos bajo demanda

- Para preparar un equipo, usar `scripts/instalar_requisitos.py`: comprueba e instala el conjunto completo de PDF/Word, imágenes, gráficos y mantenimiento desde un requirements plano, en el Python actual (3.12+), reutilizando paquetes compatibles. El aislamiento es opcional con `--entorno RUTA`; `--comprobar` diagnostica sin escribir. Funciona en Windows, Linux y macOS; no instala Python ni herramientas externas. No fuerza instalaciones sobre un Python protegido por el sistema. Ejecutarlo cuando el encargo requiera preparar dependencias, no durante cada tarea editorial. Consultar [portabilidad](references/portabilidad.md#instalador-de-requerimientos).

- Para mantenimiento, `scripts/validar_coleccion.py` reúne estructura, pruebas, dependencias y comparación de copias. Consultar [validación unificada](references/portabilidad.md#validación-unificada). No instala ni sincroniza archivos y no presenta pruebas omitidas como aprobación.
- Para publicar o actualizar el catálogo del repositorio, `scripts/generar_documentacion_skills.py` crea una ficha Markdown por cada skill visible a partir de su frontmatter, secciones y recursos reales. Requiere `--overwrite` para actualizar un destino existente y excluye entornos, cachés y bytecode.
- [references/portabilidad.md](references/portabilidad.md): ejecución, Python y pruebas.
- [references/perfiles-editoriales.md](references/perfiles-editoriales.md): políticas y formato del proyecto.
- [references/mapa-responsabilidades.md](references/mapa-responsabilidades.md): selección de especialidades.
- [references/ruta-de-trabajo.md](references/ruta-de-trabajo.md) y [references/diagnostico-por-etapa.md](references/diagnostico-por-etapa.md): orientación adicional por etapa.
- [references/migracion-27-skills.md](references/migracion-27-skills.md): equivalencias y recuperación tras la fusión; solo para mantenimiento.
- [references/auditoria-automatizacion.md](references/auditoria-automatizacion.md): registro histórico, no certificado de validez vigente.

## Cierre

En obras gobernadas por un contexto, contrastar el índice y los encabezados reales con la estructura publicable acordada. Revisar la cobertura de las instrucciones dentro del desarrollo y registrar los controles de calidad con evidencia, pendientes y conflictos fuera del manuscrito. Una exportación correcta no demuestra que esta separación se haya respetado.

Verificar que se atendió el encargo, las fuentes y datos conservan trazabilidad, el método no cambió por una skill auxiliar y las comprobaciones corresponden al producto entregado. Comunicar pendientes reales y límites de la validación.
