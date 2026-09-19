# Estructura canónica de proyectos de libro

## Principio

Crear la estructura completa al iniciar cada libro, aunque algunas carpetas permanezcan vacías. Mantener estable el significado de cada etapa; agregar subcarpetas específicas sin cambiar las carpetas raíz.

## Carpetas obligatorias

| Ruta | Responsabilidad |
|---|---|
| `00_contexto_y_diagnostico/` | Contextos maestros, originales, conversiones, segmentación, inventarios y diagnósticos iniciales |
| `01_planificacion_editorial/` | Ficha editorial, alcance, lector, índice maestro, matriz de capítulos y ruta de trabajo |
| `02_manuscrito/` | Preliminares, capítulos, cierres y manuscrito integrado en elaboración |
| `03_casos_aplicados/` | Casos integradores, situaciones de análisis, líneas de tiempo y datos de casos |
| `04_recursos_didacticos/` | Preguntas, ejercicios, actividades, cuadros de síntesis y materiales complementarios |
| `05_investigacion_bibliografia/` | Estrategias de búsqueda, fuentes activas, descartadas, metadatos, matrices de evidencia y bibliografía |
| `06_recursos_visuales/` | Imágenes, tablas, figuras, originales, manifiestos, licencias, pies y textos alternativos |
| `07_glosario_terminologia/` | Glosario, términos preferidos, variantes y decisiones terminológicas |
| `08_revision_editorial/` | Auditorías científicas, estructurales, bibliográficas, lingüísticas, visuales y de preentrega |
| `09_entregables/` | Borradores integrados, versiones revisadas y finales exportables |
| `plantillas/` | Plantillas reutilizables de capítulo, apartado, evidencia, figura y revisión |

## Subcarpetas mínimas

- `00_contexto_y_diagnostico/originales/`
- `00_contexto_y_diagnostico/preprocesado/`
- `05_investigacion_bibliografia/fuentes_activas/`
- `05_investigacion_bibliografia/fuentes_descartadas/`
- `05_investigacion_bibliografia/metadata/`
- `06_recursos_visuales/imagenes/`
- `06_recursos_visuales/originales/`
- `06_recursos_visuales/metadata/`
- `06_recursos_visuales/tablas_html/`
- `09_entregables/v01_borrador/`
- `09_entregables/v02_revision/`
- `09_entregables/v02_revision/anexos/`
- `09_entregables/v03_final_txt/`
- `09_entregables/v03_final_docx/`

## Reglas

- No guardar fuentes descartadas junto a fuentes citables activas.
- No usar `09_entregables` como área de trabajo cotidiana.
- Mantener originales y archivos derivados separados.
- Guardar el manuscrito fuente por capítulos en `02_manuscrito` y las integraciones versionadas en `09_entregables`.
- Ubicar el DOCX editable en `09_entregables/v03_final_docx/libro_completo.docx` y el TXT de respaldo en `09_entregables/v03_final_txt/libro_completo.txt`.
- Guardar en `09_entregables/v02_revision/anexos/anexo_prompts_recursos_generados.md` los prompts, modelos, fechas y razones de imágenes o tablas generadas; no mezclar este registro con el cuerpo del libro.
- Si un proyecto antiguo usa otros nombres, no mover ni borrar automáticamente. Crear un mapa de equivalencias y migrar solo con autorización expresa.
