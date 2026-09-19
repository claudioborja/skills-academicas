---
name: humanizar-redaccion-academica
description: Revisa prosa académica genérica, mecánica o fragmentada y la alinea con una voz definida, preservando evidencia, citas y desarrollo. Usar para desgenericar, recuperar continuidad o extraer y comparar perfiles de estilo; no sustituye la redacción de resultados ni la corrección ortográfica final.
---

# Humanizar Redacción Académica

Los generadores de informes y perfiles exigen `--overwrite` para reemplazar salidas existentes, nunca entradas. Requieren `workflow-maestro-academico-editorial/scripts/archivos_seguros.py`, también en ejecución directa. Consultar [protección y límites de escritura](../workflow-maestro-academico-editorial/references/portabilidad.md#protección-de-informes).

## Modos

- **Naturalidad y continuidad:** variar ritmo y arquitectura sin perder argumento; leer [references/estrategias.md](references/estrategias.md).
- **Desgenericación:** precisar alcance, mecanismo, condición y consecuencias; leer [references/patrones-de-genericidad.md](references/patrones-de-genericidad.md) y [references/tecnicas-de-especificacion.md](references/tecnicas-de-especificacion.md).
- **Voz desde documentos modelo:** extraer y comparar perfiles según [references/perfil-de-estilo.md](references/perfil-de-estilo.md). No copiar frases, experiencias ni datos del modelo.
- **Reporte externo:** interpretar señales de similitud o IA para priorizar revisión. No diagnosticar autoría, acusar plagio ni garantizar resultados frente a detectores.

Redactar contenido nuevo corresponde a `$gestor-redaccion-latinoamerica`; corregir ortografía y ortotipografía corresponde a `$correccion-estilo-ortotipografica`. Resolver primero problemas de evidencia o método con la skill especializada.

## Flujo y protección

1. Identificar el problema y el alcance. Si el insumo es largo, usar `$preprocesador-documentos` para localizar secciones.
2. Proteger citas textuales, transcripciones, referencias, DOI, URLs, tablas, datos, fórmulas, código y nombres técnicos.
3. Registrar extensión y función de los bloques: planteamiento, evidencia, explicación, contraste, ejemplo, implicación o transición.
4. Reescribir prosa propia; precisar generalidades con material disponible y variar entradas/cierres según su función. No inventar hechos, experiencias o ejemplos probatorios.
5. Conectar párrafos por continuidad conceptual; no sustituir el argumento por conectores. Fusionar fragmentos solo cuando pertenezcan al mismo movimiento argumental.
6. Verificar sentido, respaldo de citas, desarrollo y voz. No comprimir por sistema ni ampliar con relleno.
7. Entregar el texto solicitado y, cuando aporte valor, un balance breve de cambios y pendientes.

Los rangos de extensión y párrafos proceden del [perfil del proyecto](../workflow-maestro-academico-editorial/references/perfiles-editoriales.md). Son orientativos; la función y el encargo prevalecen. Si falta evidencia para desarrollar una idea, señalar el vacío.

## Herramientas reutilizables

Consultar [la guía de ejecución](../workflow-maestro-academico-editorial/references/portabilidad.md). Las rutas siguientes son relativas a esta skill:

| Herramienta | Uso y límite |
| --- | --- |
| `scripts/analizar_marcas_ia.py` | Repeticiones, conectores y fragmentación; no detecta autoría IA. Acepta `--baseline`, `--min-ratio`, `--max-ratio` y `--short-words`. |
| `scripts/analizar_reporte_compilatio.py` | Extrae señales del reporte; no interpreta automáticamente responsabilidad o plagio. |
| `scripts/documento_a_perfil_estilo.py` | Extrae un perfil desde PDF/DOCX/MD/TXT/HTML. |
| `scripts/comparar_con_perfil_estilo.py` | Compara borrador y perfil; las diferencias no son errores por sí mismas. |
| `scripts/perfilar_y_comparar_estilo.py` | Guarda datos del perfil en `styles/<nombre>/` y produce diagnóstico; `--out-dir` añade una copia auxiliar. |
| `scripts/conectar_prosa_final_txt.py` | Une mecánicamente fragmentos; exige `--out` diferente del original. Revisar el resultado con el analizador y su `--baseline`, pues unir párrafos no desarrolla ideas. |
| `scripts/auditar_respaldo_citas_pdf.py` | Busca candidatos por similitud léxica; no demuestra respaldo semántico. Puede recibir vocabulario de un dominio mediante `--vocabulary`. |
| `scripts/resumir_alertas_respaldo_citas.py` | Resume alertas pendientes de comprobación manual. |
| `scripts/limpiar_entrega_final_txt.py` | Conserva todo por defecto; solo elimina líneas elegidas con `--remove-lines N ...`. Exige `--out` diferente del original. No reescribe prosa ni decide qué es andamiaje. |

Ejemplo:

```text
python skills/workflow-maestro-academico-editorial/scripts/ejecutar.py humanizar-redaccion-academica/scripts/analizar_marcas_ia.py "ruta/editado.md" --baseline "ruta/original.md" --json
```

## Evidencia y reportes

En los dos transformadores TXT, seleccionar líneas/cambios tras revisión y conservar fuentes: no aplicar eliminación por etiquetas ni sustituciones temáticas. `--report` no puede coincidir con entrada o salida. `--overwrite` autoriza reemplazar salidas existentes, nunca originales; mediante el lanzador añadir también `--permitir-sobrescritura` antes de la ruta del script. No se generan respaldos automáticos. La escritura es atómica por archivo, no una transacción conjunta del texto y su reporte.

Antes de ejecutar la auditoría léxica, leer [references/auditoria-lexica-citas.md](references/auditoria-lexica-citas.md) para el manifiesto obligatorio y los límites de cobertura.

Una cita requiere una afirmación concreta y un pasaje que la respalde. Ante una alerta automática, abrir la fuente y comprobar contexto, negaciones, población y alcance antes de retirar, sustituir o reformular una cita. Una puntuación baja puede ser una traducción o limitación del detector; una alta puede ser coincidencia temática.

Ante un reporte externo, separar bibliografía, glosarios, diagramas, lenguaje técnico y citas de la prosa propia editable. No alterar identificadores, datos o terminología correcta porque el reporte marque un idioma distinto.

## Límites de automatización

Conservar scripts generales de análisis, extracción y transformación determinista. No programar párrafos, preguntas, títulos o transiciones de un libro concreto. Los perfiles y vocabularios se guardan como datos seleccionados para un proyecto; no se aplican a todos los manuscritos.
