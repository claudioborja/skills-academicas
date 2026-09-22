---
name: gestor-referencias-academicas
description: Busca, verifica y utiliza fuentes académicas para respaldar afirmaciones y formatear citas y bibliografía en APA 7 o IEEE. Usar para fortalecer borradores, consultar fuentes completas, organizar evidencia o cambiar de norma bibliográfica; la selección de estudios de una revisión corresponde a su protocolo.
---

# Gestor de Referencias Académicas

## Selección del modo

- **Respaldo de afirmaciones:** localizar, leer y verificar fuentes antes de incorporarlas.
- **Formato APA 7:** leer [references/apa7-practico.md](references/apa7-practico.md).
- **Formato IEEE:** leer [references/ieee-practico.md](references/ieee-practico.md).

Para presentación IEEE de un manuscrito completo, leer [la ruta de plantilla y revisión](../maquetacion-academica-preentrega/references/ieee-presentacion.md). No aplicar maquetación ni auditoría APA a una obra IEEE. Las referencias generadas desde DOI son borradores y requieren revisión por tipo de fuente.
- **Conversión de norma:** conservar las fuentes y las afirmaciones respaldadas; rehacer citas y bibliografía de forma coordinada.

Conservar la norma del manuscrito si ya es consistente. Si no hay norma identificable y afecta al resultado, solicitar ese dato. No cargar ambas guías cuando solo se use una.

Si el encargo incluye cumplimiento APA del documento completo, leer también [la guía de maquetación APA](../maquetacion-academica-preentrega/references/apa7-docx.md), distinguir trabajo estudiantil/profesional y coordinar la revisión de presentación. La corrección bibliográfica sola no certifica portada, estilo, estadística, tablas ni todo el manual. Resolver casos especiales con fuentes oficiales y declarar lo no verificado.

## Reglas comunes

No inventar autores, fechas, DOI, páginas, resultados ni citas. Abrir y leer el texto completo y el pasaje pertinente antes de respaldar una afirmación; un título, abstract o coincidencia de palabras no demuestra respaldo.

Aplicar la política del proyecto según [../editor-en-jefe/references/perfiles-editoriales.md](../editor-en-jefe/references/perfiles-editoriales.md). El perfil histórico de fuentes con DOI es una política de selección, no parte de APA o IEEE. Si solo se pide corregir formato, no buscar, excluir ni sustituir fuentes por defecto.

Con Kitchenham activo, su protocolo gobierna admisión, descarga, revisión manual y trazabilidad. Esta skill solo verifica el respaldo y da formato a fuentes admitidas; no cambia criterios de inclusión ni introduce requisitos de DOI o PRISMA.

## Flujo

Para libros, aplicar la sección de evidencia de [producción editorial integrada](../editor-en-jefe/references/produccion-editorial-eficiente.md). Antes de buscar o extraer de nuevo, consultar los originales, extracciones y decisiones del proyecto. Recuperar pasajes con contexto y localizadores; una coincidencia de búsqueda o una fuente admitida no certifica respaldo. No exigir aprobación individual del usuario salvo instrucción o protocolo. Registrar cambios que invaliden evidencia ya usada.

1. Identificar norma, política de fuentes, alcance de la intervención y carpeta del proyecto.
2. Usar `$automatizador-referencias` cuando haga falta inventariar metadatos, DOI, duplicados o correspondencia entre citas y bibliografía.
3. En modo de respaldo, identificar la afirmación concreta y sus límites; buscar fuentes pertinentes según [references/busqueda-y-descarga.md](references/busqueda-y-descarga.md).
4. Evaluar reputación y procedencia con `$filtro-editoriales-depredadoras`; distinguir una alerta de una exclusión justificada.
5. Leer la evidencia, registrar archivo/localizador y explicar qué afirmación respalda. No transferir conclusiones entre contextos sin justificación.
6. Formatear con la guía de la norma activa. En IEEE, numerar por primera aparición y reutilizar el número; en APA, mantener autor-año y datos verificables.
7. Comprobar citas frente a bibliografía con `$revisor-citas-consistencia-bibliografica` cuando el alcance lo requiera.
8. Marcar datos o respaldos pendientes. Apartar fuentes descartadas conservando trazabilidad; no borrar originales automáticamente.

## Archivos

Respetar las rutas de un protocolo o proyecto existente. En libros con estructura canónica, usar `05_investigacion_bibliografia/fuentes_activas/<norma>/` y `05_investigacion_bibliografia/metadata/<norma>/`; `<norma>` es `apa7` o `ieee`. En tareas breves, usar la carpeta elegida sin imponer una estructura de libro.

## Extractor común de PDF

Leer [../editor-en-jefe/references/portabilidad.md](../editor-en-jefe/references/portabilidad.md) para intérpretes y dependencias.

```text
python skills/editor-en-jefe/scripts/ejecutar.py gestor-referencias-academicas/scripts/pdf_a_contexto.py "ruta/fuente.pdf" --out "ruta/lectura.md" --json-out "ruta/lectura.json" --profile fuente
```

Acepta PDF, carpeta y URL directa. Para descargas, proporcionar `--download-dir` con la carpeta del proyecto. Los perfiles `fuente`, `imryd` y `tesis` solo priorizan vocabulario: no cambian el método ni verifican semánticamente la evidencia.

Las descargas HTTP(S) reciben nombre único y no reemplazan PDFs existentes; límite de 50 MiB y comprobación de firma PDF (no certifica integridad del documento). Los reportes no pueden coincidir con entradas ni entre sí; `--overwrite` permite reemplazar solo reportes. Con el lanzador, la sustitución requiere además `--permitir-sobrescritura` antes del script. Conservar la URL original registrada en el contexto; el nombre descargado no identifica por sí solo la fuente.

## Glosarios y entrega

Respaldar cada definición con una fuente pertinente y consultada; distinguir paráfrasis de cita literal y verificar localizadores. Presentar el glosario según el perfil editorial de la obra.

Entregar el texto o bibliografía solicitado, junto con pendientes relevantes. Mantener correspondencia entre citas y referencias con las excepciones de la norma (p. ej., comunicaciones personales), datos trazables y una sola norma. No presentar extracción mecánica como lectura crítica ni cero alertas como certificación integral.
