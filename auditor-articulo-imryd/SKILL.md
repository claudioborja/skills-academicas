---
name: auditor-articulo-imryd
description: Extrae secciones, fragmentos y señales mecánicas de artículos IMRyD para orientar una revisión científica. Usar para inventario estructural y checklist de envío; sus scripts no prueban coherencia entre objetivo, método y resultados ni suficiencia de evidencia.
---

# Auditor Artículo IMRyD

## Ejecución multiplataforma

Consultar [la guía común de ejecución](../editor-en-jefe/references/portabilidad.md) para elegir intérprete y preparar dependencias.

## Objetivo

Producir un diagnóstico rápido de estructura científica antes de redactar, reordenar o enviar un artículo.

## Scripts

```text
python skills/editor-en-jefe/scripts/ejecutar.py auditor-articulo-imryd/scripts/auditar_imryd.py articulo.md --out imryd.md --json-out imryd.json
python skills/editor-en-jefe/scripts/ejecutar.py auditor-articulo-imryd/scripts/matriz_objetivo_metodo_resultados.py articulo.md --out matriz.md --json-out matriz.json
python skills/editor-en-jefe/scripts/ejecutar.py auditor-articulo-imryd/scripts/check_envio_revista.py articulo.md --out envio.md --json-out envio.json
```

## Uso

Las expresiones regulares identifican encabezados y palabras, no relaciones científicas. "No detectado" significa ausencia de una coincidencia, no ausencia demostrada de contenido. Comprobar manualmente los pasajes antes de concluir desalineación, falta de evidencia o aptitud para envío. La matriz es una extracción de candidatos, no una evaluación semántica.

Ejecutar después de `$preprocesador-documentos`. Usar el reporte para orientar `$redaccion-articulo-cientifico-imryd` y evitar que el agente lea todo el artículo si solo necesita saber qué sección falla.
