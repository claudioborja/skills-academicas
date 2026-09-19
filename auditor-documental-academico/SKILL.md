---
name: auditor-documental-academico
description: "Inventaria y audita mecánicamente documentos académicos o editoriales para reducir lectura manual: estructura, encabezados, extensión por sección, tablas, figuras, citas, bibliografía, terminología, anexos y checklist de preentrega. Use when Codex needs to prepare compact reports for workflow-maestro-academico-editorial, convertidor-tesis-a-libro, redaccion-articulo-cientifico-imryd, gestor-tablas-figuras-pies, normalizador-terminologia-glosario or maquetacion-academica-preentrega."
---

# Auditor Documental Académico

## Ejecución multiplataforma

Consultar [la guía común de ejecución](../workflow-maestro-academico-editorial/references/portabilidad.md) para elegir intérprete y preparar dependencias.

## Objetivo

Generar inventarios compactos para que el agente no tenga que leer un manuscrito completo antes de decidir qué corregir, reordenar o revisar.

## Scripts

```text
python skills/workflow-maestro-academico-editorial/scripts/ejecutar.py auditor-documental-academico/scripts/inventariar_documento.py manuscrito.md --out inventario.md --json-out inventario.json
python skills/workflow-maestro-academico-editorial/scripts/ejecutar.py auditor-documental-academico/scripts/inventariar_tablas_figuras.py manuscrito.md --out visual.md --json-out visual.json
python skills/workflow-maestro-academico-editorial/scripts/ejecutar.py auditor-documental-academico/scripts/auditar_terminologia.py manuscrito.md --terms "aprendizaje automático" "machine learning" --out terminos.md --json-out terminos.json
python skills/workflow-maestro-academico-editorial/scripts/ejecutar.py auditor-documental-academico/scripts/check_preentrega.py manuscrito.md --out preentrega.md --json-out preentrega.json
python skills/workflow-maestro-academico-editorial/scripts/ejecutar.py auditor-documental-academico/scripts/analizar_repeticiones.py manuscrito.md --out repeticiones.md --json-out repeticiones.json
```

## Uso

Interpretar los reportes como inventarios y alertas heurísticas. No certifican exhaustividad, respaldo bibliográfico ni calidad editorial. Revisar manualmente los hallazgos y las secciones relevantes; la ausencia de una coincidencia no demuestra una omisión.

Ejecutar después de `$preprocesador-documentos` cuando el documento ya esté en Markdown o texto plano. Usar los reportes para decidir si conviene activar tablas/figuras, terminología, preentrega, coherencia o redacción.
